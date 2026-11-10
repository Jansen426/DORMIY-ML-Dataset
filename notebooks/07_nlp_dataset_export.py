"""
Script: 07_nlp_dataset_export.py
Deskripsi: Pipeline Kurasi, Penyaringan Kata Kunci Negatif, Validasi Ketat Integritas,
           dan Ekspor Dataset NLP DORMIY berdasarkan kriteria kurasi pada
           final_dataset_curation_criteria.md, hasil audit pada final_curation_audit.md,
           dan temuan inspeksi pilot_image_visual_review.md.

Aturan & Logika Kurasi Jalur A (NLP):
1. Mengambil seluruh 344 produk dengan relevance_label == 'Relevant' dari data/processed/dormiy_products_clean.csv.
2. Membaca tabel utama pilot review secara ketat (validasi tepat 20 ID pilot yang terdaftar resmi:
   9 Keep, 4 Manual Review, 7 Exclude).
3. Mengintegrasikan 7 produk berstatus Exclude dari pilot review sebagai pengecualian yang sudah
   terkonfirmasi (status: 'Excluded_NLP'). Ketujuh produk ini dikeluarkan dari katalog kandidat.
4. Menerapkan Negative Keyword Screening terhadap judul, deskripsi, kategori, dan brand untuk mendeteksi
   produk yang terindikasi tidak sesuai dengan inventaris asrama (rokok/tembakau, senjata tajam/taktis, perlengkapan bayi,
   mesin industri spesifik, suku cadang kendaraan pribadi), dengan penanganan pluralitas knife/knives secara akurat.
5. Produk yang terdeteksi oleh negative keyword screening TETAPI belum memiliki keputusan Exclude terkonfirmasi
   diberi status 'Candidate_Review' (bukan otomatis dikeluarkan), agar dapat ditinjau lebih lanjut oleh tim.
6. Produk yang sudah benar-benar diverifikasi secara manual memiliki relevansi tekstual untuk inventaris asrama
   diberi status 'Approved_NLP':
   - 9 produk pilot berstatus Keep yang relevan untuk asrama (prod_0792, prod_0238, prod_0394, prod_0235,
     prod_0474, prod_0510, prod_0786, prod_0719, prod_0064).
   - 2 produk pilot berstatus Manual Review untuk CV yang teksnya terkonfirmasi relevan (prod_0741 & prod_0569).
7. Produk lainnya yang belum diperiksa secara manual dan lolos negative keywords diberi status 'Candidate_NLP'.
8. Produk Maybe Relevant dan Irrelevant tidak dimasukkan secara otomatis. Nilai data cleaned sumber tidak diubah.
9. Memvalidasi ketiadaan perubahan data sumber sebelum dan sesudah eksekusi (data, kolom, dan baris tetap utuh).
10. Memastikan standar JSON bebas dari NaN (seluruh NaN dikonversi menjadi None/null).
11. Memvalidasi rekonsiliasi detail seluruh atribut record per record antara file CSV dan JSON.
12. Menghasilkan laporan dinamis tanpa angka hardcoded.
"""

import hashlib
import json
import os
import re
import sys
import pandas as pd

# Konfigurasi Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "dormiy_products_clean.csv")
PILOT_REVIEW_PATH = os.path.join(BASE_DIR, "reports", "pilot_image_visual_review.md")

OUTPUT_DIR = os.path.join(BASE_DIR, "data", "final")
OUTPUT_CSV_PATH = os.path.join(OUTPUT_DIR, "dormiy_nlp_catalog.csv")
OUTPUT_JSON_PATH = os.path.join(OUTPUT_DIR, "dormiy_nlp_catalog.json")
REPORT_PATH = os.path.join(BASE_DIR, "reports", "nlp_dataset_export_summary.md")

# 20 Product ID Pilot yang Ditetapkan Resmi Berdasarkan Hasil Visual Review
EXPECTED_PILOT_PIDS = {
    "prod_0569", "prod_0583", "prod_0659", "prod_0792",
    "prod_0802", "prod_0008", "prod_0273", "prod_0238",
    "prod_0394", "prod_0751", "prod_0892", "prod_0235",
    "prod_0741", "prod_0474", "prod_0672", "prod_0510",
    "prod_0054", "prod_0786", "prod_0719", "prod_0064",
}

# Kolom Output Spesifikasi Minimal untuk NLP
OUTPUT_COLUMNS = [
    "product_id",
    "title",
    "clean_title",
    "text_for_nlp",
    "main_category",
    "sub_category",
    "brand_imputed",
    "is_secondhand",
    "relevance_label",
    "needs_review",
    "curation_status",
    "curation_reason",
]

# Definisi Negative Keyword Screening Patterns
# Pola knife diperbaiki agar mencocokkan knife dan knives (misal pocket knife / pocket knives)
NEGATIVE_KEYWORD_PATTERNS = {
    "tobacco_smoking": (
        r"\b(rolling\s+papers?|cigarettes?|cigars?|tobaccos?|hookahs?|bongs?|vapes?|vapings?|ash\s*trays?)\b",
        "Terdeteksi indikasi produk konsumsi tembakau/rokok/vaping",
    ),
    "weapons_tactical": (
        r"\b(pocket\s+kni(?:fe|ves)|tactical\s+kni(?:fe|ves)|folding\s+kni(?:fe|ves)|hunting\s+kni(?:fe|ves)|machetes?|daggers?|swords?|combat\s+kni(?:fe|ves)|ammunitions?|ammo)\b",
        "Terdeteksi indikasi pisau taktis/senjata tajam di luar perlengkapan makan/dapur",
    ),
    "infant_baby": (
        r"\b(highchairs?|bassinets?|strollers?|cribs?|baby\s+carriers?|diapers?|pacifiers?|breast\s+pumps?|lasten\s+sängynrunko)\b",
        "Terdeteksi indikasi perabot/perlengkapan bayi & anak kecil di luar profil asrama umum",
    ),
    "heavy_industrial_specialized": (
        r"\b(tabbers?|terminal\s+blocks?|pcb\s+connectors?|police\s+scanners?|garden\s+arch\s+arbors?)\b",
        "Terdeteksi indikasi mesin industri berat/komponen sirkuit murni/instalasi taman spesifik",
    ),
    "automotive_parts": (
        r"\b(car\s+gps|head-up\s+displays?|hud\s+displays?|obd2|spark\s+plugs?|carburetors?)\b",
        "Terdeteksi indikasi aksesoris/suku cadang kendaraan pribadi di luar fasilitas gedung",
    ),
}


def compute_file_hash(filepath: str) -> str:
    """Menghitung SHA-256 hash dari file untuk memastikan integritas file tidak berubah."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_pilot_review_results(review_path: str) -> dict:
    """Membaca HANYA tabel utama hasil keputusan visual review dari reports/pilot_image_visual_review.md.

    Melakukan validasi ketat:
    - 20 product_id pilot sama persis dengan EXPECTED_PILOT_PIDS (tidak boleh ada yang hilang, berbeda, atau bertambah).
    - Jumlah keputusan Keep = 9, Manual Review = 4, dan Exclude = 7.
    - Hentikan proses jika format atau ID keputusan tidak sesuai.
    """
    if not os.path.exists(review_path):
        raise FileNotFoundError(f"File pilot review tidak ditemukan: {review_path}")

    pilot_reviews = {}
    in_table_section = False

    with open(review_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()

            # Tandai awal seksi tabel evaluasi per produk
            if line_str.startswith("## 1. Hasil Visual Inspection"):
                in_table_section = True
                continue

            # Akhiri pembacaan tabel jika masuk ke seksi ringkasan berikutnya
            if in_table_section and line_str.startswith("## 2. Ringkasan"):
                in_table_section = False
                break

            # Hanya baca baris data produk di dalam tabel utama
            if in_table_section and line_str.startswith("|") and "`prod_" in line_str:
                parts = [p.strip().replace(chr(96), "") for p in line_str.split("|")[1:-1]]
                if len(parts) >= 8:
                    pid = parts[0]
                    pilot_reviews[pid] = {
                        "title": parts[1],
                        "image_type": parts[2],
                        "visual_match": parts[3],
                        "image_quality": parts[4],
                        "dorm_inventory_relevance": parts[5],
                        "reason": parts[6],
                        "recommended_action": parts[7],
                    }

    # 1. Validasi Total Jumlah Produk yang Terbaca
    total_parsed = len(pilot_reviews)
    if total_parsed != 20:
        raise ValueError(
            f"Validasi Gagal pada {review_path}: Diharapkan 20 produk pada tabel utama, "
            f"ditemukan {total_parsed} produk."
        )

    # 2. Validasi Identitas Set 20 product_id Sama Persis
    parsed_pids = set(pilot_reviews.keys())
    missing_pids = EXPECTED_PILOT_PIDS - parsed_pids
    unexpected_pids = parsed_pids - EXPECTED_PILOT_PIDS
    if missing_pids or unexpected_pids:
        raise ValueError(
            f"Validasi Gagal pada ID pilot review: "
            f"ID hilang: {missing_pids}, ID tidak terduga: {unexpected_pids}."
        )

    # 3. Validasi Komposisi Keputusan
    actions_count = {}
    for pid, data in pilot_reviews.items():
        act = data["recommended_action"]
        actions_count[act] = actions_count.get(act, 0) + 1

    expected_actions = {"Keep": 9, "Manual Review": 4, "Exclude": 7}
    for act, exp_count in expected_actions.items():
        actual_count = actions_count.get(act, 0)
        if actual_count != exp_count:
            raise ValueError(
                f"Validasi Gagal pada keputusan pilot review: Keputusan '{act}' bernilai {actual_count}, "
                f"tetapi diharapkan tepat {exp_count}."
            )

    return pilot_reviews


def check_negative_keywords(row: pd.Series) -> list:
    """Memeriksa teks judul, deskripsi, kategori, dan brand terhadap pola kata kunci negatif."""
    full_text = f"{row['title']} {row['category']} {row['brand_imputed']} {row['text_for_nlp']}"
    detected_reasons = []

    for cat_name, (pat, desc) in NEGATIVE_KEYWORD_PATTERNS.items():
        if re.search(pat, full_text, flags=re.IGNORECASE):
            detected_reasons.append(desc)

    return detected_reasons


def assign_nlp_curation(row: pd.Series, pilot_reviews: dict) -> tuple:
    """Menentukan status kurasi NLP dan alasannya sesuai spesifikasi kurasi DORMIY.

    Status Kurasi:
    - Excluded_NLP: Terkonfirmasi Exclude dari pilot review (dikeluarkan dari katalog).
    - Approved_NLP: Terkonfirmasi relevan secara manual untuk inventaris asrama.
    - Candidate_Review: Terdeteksi screening kata kunci negatif / perkakas teknis, memerlukan peninjauan kurator.
    - Candidate_NLP: Kandidat awal yang belum diperiksa dan lolos screening kata kunci negatif.
    """
    pid = row["product_id"]

    # 1. Pengecualian Terkonfirmasi (7 produk Exclude dari Pilot Review)
    if pid in pilot_reviews:
        review = pilot_reviews[pid]
        action = review["recommended_action"]
        drel = review["dorm_inventory_relevance"]

        if action == "Exclude":
            return "Excluded_NLP", f"Eksklusi terkonfirmasi (Pilot Review): {review['reason']}"

        if action == "Keep" and drel == "Relevant":
            return "Approved_NLP", "Terkonfirmasi relevan untuk inventaris asrama (Pilot Review)"

        if action == "Manual Review":
            if pid in ["prod_0741", "prod_0569"]:
                return "Approved_NLP", (
                    "Terkonfirmasi relevan secara tekstual untuk inventaris asrama "
                    f"(Manual review CV karena visual: {review['reason']})"
                )
            # prod_0802 & prod_0273 adalah perkakas bengkel pemeliharaan
            return "Candidate_Review", (
                "Perkakas pemeliharaan teknis fasilitas asrama; memerlukan peninjauan "
                "kebijakan operasional asrama"
            )

    # 2. Negative Keyword Screening untuk produk yang belum memiliki keputusan manual terkonfirmasi
    negative_hits = check_negative_keywords(row)
    if negative_hits:
        combined_reasons = "; ".join(negative_hits)
        return "Candidate_Review", f"Terdeteksi screening kata kunci negatif: {combined_reasons}"

    # 3. Produk kandidat awal yang lolos screening kata kunci negatif (menunggu kurasi manual)
    return "Candidate_NLP", "Kandidat awal kategori relevan; lolos screening kata kunci negatif"


def build_and_export_nlp_catalog():
    """Fungsi utama untuk memproses, memvalidasi secara ketat, dan mengekspor katalog dataset NLP."""
    print("=" * 75)
    print("DORMIY - NLP Dataset Export & Validation Pipeline (Revisi Ketat)")
    print("=" * 75)

    # 1. Verifikasi Eksistensi & Catat Hash Sumber Sebelum Proses
    if not os.path.exists(CLEANED_DATA_PATH):
        raise FileNotFoundError(f"File data cleaned tidak ditemukan: {CLEANED_DATA_PATH}")

    src_hash_before = compute_file_hash(CLEANED_DATA_PATH)
    df_cleaned_before = pd.read_csv(CLEANED_DATA_PATH)
    original_shape = df_cleaned_before.shape
    original_columns = df_cleaned_before.columns.tolist()

    print(f"[INFO] Membaca dataset cleaned: {original_shape[0]} baris, {original_shape[1]} kolom.")

    # 2. Filter 344 Produk dengan relevance_label == 'Relevant'
    df_relevant = df_cleaned_before[df_cleaned_before["relevance_label"] == "Relevant"].copy()
    total_relevant = len(df_relevant)
    print(f"[INFO] Kandidat awal (relevance_label == 'Relevant'): {total_relevant} produk.")

    if total_relevant != 344:
        raise ValueError(
            f"Validasi Gagal: Total kandidat awal seharusnya 344, ditemukan {total_relevant}."
        )

    # 3. Baca Tabel Pilot Review dengan Validasi Ketat (20 produk: 9 Keep, 4 Manual Review, 7 Exclude)
    pilot_reviews = load_pilot_review_results(PILOT_REVIEW_PATH)
    print(
        f"[INFO] Validasi tabel pilot review berhasil: Tepat 20 ID pilot terverifikasi "
        "(9 Keep, 4 Manual Review, 7 Exclude)."
    )

    # 4. Terapkan Logika Kurasi & Screening Kata Kunci Negatif
    statuses = []
    reasons = []

    for _, row in df_relevant.iterrows():
        status, reason = assign_nlp_curation(row, pilot_reviews)
        statuses.append(status)
        reasons.append(reason)

    df_relevant["curation_status"] = statuses
    df_relevant["curation_reason"] = reasons

    # 5. Hitung Distribusi Aktual Status Kurasi
    status_counts = df_relevant["curation_status"].value_counts().to_dict()
    n_approved = status_counts.get("Approved_NLP", 0)
    n_candidate_nlp = status_counts.get("Candidate_NLP", 0)
    n_candidate_rev = status_counts.get("Candidate_Review", 0)
    n_excluded = status_counts.get("Excluded_NLP", 0)

    print("\n[INFO] Distribusi Aktual Kurasi Status NLP:")
    print(f"  - Approved_NLP     : {n_approved} produk (Terkonfirmasi relevan manual)")
    print(f"  - Candidate_NLP    : {n_candidate_nlp} produk (Lolos screening kata kunci negatif)")
    print(f"  - Candidate_Review : {n_candidate_rev} produk (Perlu review manual: perkakas teknis / kata kunci)")
    print(f"  - Excluded_NLP     : {n_excluded} produk (Eksklusi terkonfirmasi dari pilot)")

    # 6. Pisahkan Katalog Kandidat NLP (Exclude 7 produk Excluded_NLP)
    df_catalog = df_relevant[df_relevant["curation_status"] != "Excluded_NLP"].copy()
    df_excluded = df_relevant[df_relevant["curation_status"] == "Excluded_NLP"].copy()

    total_catalog = len(df_catalog)
    print(f"\n[INFO] Total produk masuk katalog kandidat NLP: {total_catalog} produk (344 - {n_excluded}).")

    # 7. Validasi Wajib Integritas Dataset
    print("\n[VALIDASI] Menjalankan validasi wajib integritas dataset...")

    # Validasi 1: Total kandidat awal
    assert total_relevant == 344, "Total kandidat awal bukan 344!"

    # Validasi 2: Pastikan 7 produk Excluded_NLP tidak masuk katalog
    excluded_pids = set(df_excluded["product_id"])
    catalog_pids = set(df_catalog["product_id"])
    overlap = catalog_pids.intersection(excluded_pids)
    if overlap:
        raise ValueError(f"Validasi Gagal: Ditemukan produk Exclude di dalam katalog: {overlap}")
    assert len(excluded_pids) == 7, f"Jumlah produk Exclude seharusnya 7, ditemukan {len(excluded_pids)}."
    print("  [PASSED] Seluruh produk Excluded_NLP dipastikan tidak masuk katalog kandidat.")

    # Validasi 3: Ketiadaan duplikasi product_id
    if df_catalog["product_id"].duplicated().any():
        dups = df_catalog[df_catalog["product_id"].duplicated()]["product_id"].tolist()
        raise ValueError(f"Validasi Gagal: Ditemukan duplikasi product_id: {dups}")
    print("  [PASSED] Tidak ada duplikasi product_id pada katalog.")

    # Validasi 4: Ketiadaan text_for_nlp kosong
    null_texts = df_catalog["text_for_nlp"].isna().sum()
    empty_texts = (df_catalog["text_for_nlp"].str.strip() == "").sum()
    if null_texts > 0 or empty_texts > 0:
        raise ValueError(f"Validasi Gagal: Ditemukan {null_texts + empty_texts} text_for_nlp kosong.")
    print("  [PASSED] Seluruh produk memiliki text_for_nlp valid (tidak ada null/string kosong).")

    # Validasi 5: Kolom output sesuai spesifikasi minimal
    missing_cols = [c for c in OUTPUT_COLUMNS if c not in df_catalog.columns]
    if missing_cols:
        raise ValueError(f"Validasi Gagal: Kolom spesifikasi tidak ditemukan: {missing_cols}")
    df_catalog_out = df_catalog[OUTPUT_COLUMNS].copy()
    print(f"  [PASSED] Kolom output sesuai spesifikasi ({len(OUTPUT_COLUMNS)} kolom).")

    # 8. Ekspor File Output
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Ekspor CSV
    df_catalog_out.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8")
    print(f"\n[OUTPUT] CSV katalog NLP tersimpan di: {OUTPUT_CSV_PATH}")

    # Ekspor JSON (Standar JSON Murni: NaN dikonversi menjadi None agar tersimpan sebagai null)
    df_catalog_clean_json = df_catalog_out.copy()
    df_catalog_clean_json = df_catalog_clean_json.map(lambda x: None if pd.isna(x) else x)
    catalog_dict = df_catalog_clean_json.to_dict(orient="records")

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog_dict, f, ensure_ascii=False, indent=2)
    print(f"[OUTPUT] JSON katalog NLP tersimpan di: {OUTPUT_JSON_PATH} (Standar null valid)")

    # 9. Validasi Ketat Antara CSV dan JSON (Record-by-Record & Attribute-by-Attribute)
    print("\n[VALIDASI] Rekonsiliasi mendalam atribut per atribut antara CSV dan JSON...")
    df_from_csv = pd.read_csv(OUTPUT_CSV_PATH)
    with open(OUTPUT_JSON_PATH, "r", encoding="utf-8") as f:
        json_records = json.load(f)

    if len(df_from_csv) != len(json_records):
        raise ValueError(
            f"Validasi Gagal: Jumlah baris CSV ({len(df_from_csv)}) dan JSON ({len(json_records)}) berbeda!"
        )

    json_dict_by_pid = {r["product_id"]: r for r in json_records}
    if len(json_dict_by_pid) != len(json_records):
        raise ValueError("Validasi Gagal: Terdeteksi duplikasi product_id pada file JSON!")

    for _, row in df_from_csv.iterrows():
        pid = row["product_id"]
        if pid not in json_dict_by_pid:
            raise ValueError(f"Validasi Gagal: Product ID {pid} dari CSV tidak ditemukan pada JSON!")

        j_rec = json_dict_by_pid[pid]
        for col in OUTPUT_COLUMNS:
            val_csv = row[col]
            val_json = j_rec[col]

            # Normalisasi perbandingan untuk boolean / None / string
            if pd.isna(val_csv) and (val_json is None or val_json == ""):
                continue
            if isinstance(val_csv, (bool, int, float)) and isinstance(val_json, (bool, int, float)):
                if val_csv != val_json:
                    raise ValueError(
                        f"Ketidakcocokan nilai numerik/boolean pada {pid} kolom {col}: CSV={val_csv}, JSON={val_json}"
                    )
            elif str(val_csv).strip() != str(val_json).strip():
                raise ValueError(
                    f"Ketidakcocokan nilai teks pada {pid} kolom {col}: CSV='{val_csv}', JSON='{val_json}'"
                )

    print(
        f"  [PASSED] Seluruh {len(df_from_csv)} record dan {len(OUTPUT_COLUMNS)} atribut "
        "terbukti identik 100% antara CSV dan JSON."
    )

    # 10. Validasi Integritas Data Sumber (Sebelum vs Sesudah Proses)
    print("\n[VALIDASI] Memeriksa perlindungan integritas dataset cleaned...")
    src_hash_after = compute_file_hash(CLEANED_DATA_PATH)
    df_cleaned_after = pd.read_csv(CLEANED_DATA_PATH)

    if src_hash_before != src_hash_after:
        raise ValueError(
            f"Validasi Kritis Gagal: Hash file cleaned berubah selama eksekusi script! "
            f"Before: {src_hash_before}, After: {src_hash_after}"
        )
    if original_shape != df_cleaned_after.shape:
        raise ValueError(
            f"Validasi Kritis Gagal: Dimensi cleaned berubah! Before: {original_shape}, After: {df_cleaned_after.shape}"
        )
    if original_columns != df_cleaned_after.columns.tolist():
        raise ValueError("Validasi Kritis Gagal: Daftar kolom file cleaned berubah!")

    print(
        f"  [PASSED] Dataset sumber cleaned terverifikasi utuh tanpa perubahan "
        f"({original_shape[0]} baris, {original_shape[1]} kolom, hash identik)."
    )

    # 11. Buat Dokumen Ringkasan Ekspor Berdasarkan Hasil Aktual
    generate_summary_report(
        total_relevant=total_relevant,
        n_approved=n_approved,
        n_candidate_nlp=n_candidate_nlp,
        n_candidate_rev=n_candidate_rev,
        n_excluded=n_excluded,
        df_catalog=df_catalog_out,
        df_excluded=df_excluded,
        df_relevant=df_relevant,
    )
    print(f"\n[OUTPUT] Laporan ringkasan ekspor tersimpan di: {REPORT_PATH}")
    print("=" * 75)
    print("Ekspor Dataset NLP Berhasil Diselesaikan.")
    print("=" * 75)


def generate_summary_report(
    total_relevant: int,
    n_approved: int,
    n_candidate_nlp: int,
    n_candidate_rev: int,
    n_excluded: int,
    df_catalog: pd.DataFrame,
    df_excluded: pd.DataFrame,
    df_relevant: pd.DataFrame,
):
    """Membuat laporan markdown ringkasan ekspor dataset NLP secara dinamis dari hasil aktual."""
    total_catalog = len(df_catalog)
    pct_approved = (n_approved / total_relevant) * 100 if total_relevant else 0.0
    pct_candidate_nlp = (n_candidate_nlp / total_relevant) * 100 if total_relevant else 0.0
    pct_candidate_rev = (n_candidate_rev / total_relevant) * 100 if total_relevant else 0.0
    pct_excluded = (n_excluded / total_relevant) * 100 if total_relevant else 0.0
    pct_catalog = (total_catalog / total_relevant) * 100 if total_relevant else 0.0

    df_approved = df_relevant[df_relevant["curation_status"] == "Approved_NLP"]
    df_review = df_relevant[df_relevant["curation_status"] == "Candidate_Review"]

    report_content = f"""# Laporan Ekspor Dataset NLP DORMIY

**Tanggal:** 10 November 2026  
**File Output CSV:** [`data/final/dormiy_nlp_catalog.csv`](file:///D:/Dormiy-ML/data/final/dormiy_nlp_catalog.csv)  
**File Output JSON:** [`data/final/dormiy_nlp_catalog.json`](file:///D:/Dormiy-ML/data/final/dormiy_nlp_catalog.json)  
**Dataset Sumber:** [`data/processed/dormiy_products_clean.csv`](file:///D:/Dormiy-ML/data/processed/dormiy_products_clean.csv) (1.000 produk)  
**Dokumen Standar:** [`reports/final_dataset_curation_criteria.md`](file:///D:/Dormiy-ML/reports/final_dataset_curation_criteria.md) & [`reports/final_curation_audit.md`](file:///D:/Dormiy-ML/reports/final_curation_audit.md)

---

## 1. Ringkasan Eksekutif Ekspor

Dataset katalog NLP ini diekspor khusus untuk mendukung kebutuhan **Natural Language Processing (Pencarian Semantik, Keyword Search BM25, dan Text Embedding)** pada sistem inventaris asrama DORMIY. Sesuai prinsip *Dual-Track Architecture*, dataset NLP berfokus pada kualitas metadata tekstual (`clean_title`, `text_for_nlp`, `brand_imputed`, `main_category`, `sub_category`).

Seluruh angka dan persentase dihitung secara dinamis dari hasil aktual kurasi dan screening:

| Status Kurasi NLP | Jumlah Produk | Persentase dari {total_relevant} | Keterangan & Tindak Lanjut |
| :--- | :---: | :---: | :--- |
| **Approved_NLP** | **{n_approved}** | **{pct_approved:.1f}%** | **Terkonfirmasi Relevan:** Diverifikasi manual memiliki teks yang sangat relevan untuk operasional/fasilitas asrama. |
| **Candidate_NLP** | **{n_candidate_nlp}** | **{pct_candidate_nlp:.1f}%** | **Kandidat Bersih:** Lolos screening kata kunci negatif, menunggu kurasi manual bertahap. |
| **Candidate_Review** | **{n_candidate_rev}** | **{pct_candidate_rev:.1f}%** | **Kandidat Butuh Review:** Terdeteksi screening kata kunci negatif / perkakas bengkel pemeliharaan (tidak otomatis dikeluarkan). |
| **Excluded_NLP (Dikeluarkan)** | **{n_excluded}** | **{pct_excluded:.1f}%** | **Eksklusi Terkonfirmasi:** Dipastikan tidak relevan untuk asrama berdasarkan hasil inspeksi pilot. |
| **TOTAL KATALOG KANDIDAT NLP** | **{total_catalog}** | **{pct_catalog:.1f}%** | Terdiri dari `Approved_NLP`, `Candidate_NLP`, dan `Candidate_Review`. |

> [!NOTE]
> Nilai `relevance_label` pada data sumber (`dormiy_products_clean.csv`) tetap dipertahankan 100% tanpa perubahan (*zero data loss*). Seluruh keputusan kurasi dicatat secara eksplisit pada kolom `curation_status` dan `curation_reason`.

---

## 2. Rincian Produk Approved_NLP ({n_approved} Produk)

Produk-produk ini telah diverifikasi secara manual memiliki relevansi tekstual langsung dengan fasilitas dan operasional asrama:

| product_id | main_category | title | Alasan Persetujuan NLP |
| :--- | :--- | :--- | :--- |
"""
    for _, r in df_approved.iterrows():
        report_content += (
            f"| `{r['product_id']}` | {r['main_category']} | {r['title'][:60]} | {r['curation_reason']} |\n"
        )

    report_content += f"""
---

## 3. Rincian Produk Candidate_Review ({n_candidate_rev} Produk)

Produk-produk ini **tidak langsung dikeluarkan secara sepihak**, melainkan ditandai untuk peninjauan manual khusus karena terdeteksi pola kata kunci negatif atau merupakan perkakas pemeliharaan teknis:

| product_id | main_category | title | Alasan Peninjauan (curation_reason) |
| :--- | :--- | :--- | :--- |
"""
    for _, r in df_review.iterrows():
        report_content += (
            f"| `{r['product_id']}` | {r['main_category']} | {r['title'][:60]} | {r['curation_reason']} |\n"
        )

    report_content += f"""
---

## 4. Rincian Produk Excluded_NLP ({n_excluded} Produk yang Dikeluarkan)

Produk-produk ini berasal dari kandidat awal `Relevant`, namun dipastikan keluar dari katalog NLP berdasarkan keputusan review pilot yang terkonfirmasi:

| product_id | main_category | title | Alasan Eksklusi |
| :--- | :--- | :--- | :--- |
"""
    for _, r in df_excluded.iterrows():
        report_content += (
            f"| `{r['product_id']}` | {r['main_category']} | {r['title'][:60]} | {r['curation_reason']} |\n"
        )

    report_content += f"""
---

## 5. Distribusi Kategori pada Katalog Kandidat NLP ({total_catalog} Produk)

| Kategori Utama | Approved_NLP | Candidate_NLP | Candidate_Review | Total Katalog NLP | Proporsi (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""
    cat_cross = pd.crosstab(df_catalog["main_category"], df_catalog["curation_status"]).to_dict(
        orient="index"
    )
    for cat, counts in cat_cross.items():
        app = counts.get("Approved_NLP", 0)
        can = counts.get("Candidate_NLP", 0)
        rev = counts.get("Candidate_Review", 0)
        tot = app + can + rev
        pct = (tot / total_catalog) * 100 if total_catalog else 0.0
        report_content += (
            f"| **{cat}** | {app} | {can} | {rev} | **{tot}** | {pct:.1f}% |\n"
        )

    report_content += f"""| **TOTAL** | **{n_approved}** | **{n_candidate_nlp}** | **{n_candidate_rev}** | **{total_catalog}** | **100.0%** |

---

## 6. Hasil Uji Validasi Integritas Data

1. **Jumlah Kandidat Awal:** Tepat {total_relevant} produk terverifikasi dari `dormiy_products_clean.csv`.
2. **Keluaran Produk Excluded:** Seluruh {n_excluded} produk `Excluded_NLP` dipastikan 100% tidak ada di dalam `dormiy_nlp_catalog.csv` maupun `.json`.
3. **Keunikan ID:** Nol duplikasi pada kolom `product_id`.
4. **Kelengkapan Teks:** Nol nilai kosong (`NaN` atau string kosong) pada kolom `text_for_nlp`.
5. **Kesesuaian Kolom:** Seluruh {len(OUTPUT_COLUMNS)} kolom wajib tersedia (`{", ".join(OUTPUT_COLUMNS)}`).
6. **Konsistensi Format:** File CSV dan JSON telah divalidasi atribut per atribut untuk seluruh {total_catalog} entri dan terbukti 100% identik.
7. **Perlindungan Data Mentah:** File sumber `dormiy_products_clean.csv` diverifikasi utuh sebelum dan sesudah eksekusi melalui verifikasi dimensi dan checksum SHA-256.
"""
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_content)


if __name__ == "__main__":
    build_and_export_nlp_catalog()
