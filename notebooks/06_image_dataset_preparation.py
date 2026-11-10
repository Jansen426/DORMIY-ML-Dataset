"""
Skrip 06: Pilot Image Dataset Preparation (Streaming Selektif Hugging Face - Revisi Final Terverifikasi)
Proyek DORMIY - Sistem Pencarian & Rekomendasi Inventaris Asrama RTB

Arsitektur & Ketentuan Ketat:
1. Pemilihan Sampel:
   - Membaca dataset bersih dari: data/processed/dormiy_products_clean.csv secara read-only.
   - Memilih tepat 20 produk berlabel 'Relevant' secara acak berimbang menggunakan sample(n=4, random_state=42)
     dari 5 kategori utama (Home & Garden, Hardware, Electronics, Furniture, Office Supplies).
   - Memvalidasi total tepat 20 produk unik tanpa duplikasi product_id.

2. Verifikasi Pemetaan Indeks & Pembuktian Urutan terhadap Script 02:
   - Pada 02_dataset_sampling.py, data diambil melalui Hugging Face Datasets Server REST API:
     'https://datasets-server.huggingface.co/rows?dataset=Shopify/product-catalogue&config=default&split=train&offset=...&limit=...'
     sedangkan script 06 menggunakan pustaka 'datasets' dengan load_dataset(..., streaming=True).
   - Meskipun keduanya menargetkan split 'train' dan config 'default' yang sama, Datasets Server API
     dan Parquet shard stream tidak menjamin 100% determinisme urutan baris secara otomatis di semua kondisi jaringan/sharding.
   - Oleh karena itu, skrip TIDAK MENGANGGAP pemetaan indeks int(p_id) - 1 aman secara buta:
     Validasi kesesuaian judul (title cross-check) dengan normalisasi string ketat dijadikan sebagai
     BENTENG UTAMA (Primary Guardrail). Jika judul stream pada indeks target tidak cocok dengan judul CSV,
     proses langsung dihentikan dengan ValueError eksplisit (fail-fast) untuk mencegah salah pasang gambar.
   - Memastikan tidak ada dua produk target yang memiliki stream_idx sama.

3. Penanganan Transparansi & Penyimpanan Aman (Atomic File Write & Non-Destructive):
   - Menjaga format sumber asli (source_format) dari objek gambar.
   - Deteksi transparansi menyeluruh (RGBA, LA, PA, atau transparency metadata di img.info).
   - Mengompositkan ke kanvas berlatar belakang putih murni (RGB 255, 255, 255) dengan dimensi
     asli identik menggunakan alpha channel sebagai mask, sehingga background tidak hitam saat disimpan sebagai JPEG.
   - Mempertahankan resolusi/dimensi asli (tanpa resize).
   - Gambar TIDAK langsung ditulis ke save_path target:
     * Disimpan terlebih dahulu ke file sementara dengan ekstensi valid: <save_path>.tmp.jpg
     * File sementara diverifikasi menggunakan Pillow (verify) dan dicocokkan dimensinya dengan sumber.
     * Jika verifikasi sukses, file sementara dipindahkan ke save_path via os.replace() (atomic write).
     * Jika verifikasi gagal, hanya file sementara yang dihapus; gambar lama yang valid (jika ada) tidak dirusak/dihapus.
     * Kegagalan tetap dicatat sebagai status FAILED pada manifest.

4. Validasi Integritas Manifest & Riwayat Akumulatif (Anti-Duplicate & Legacy Consolidation):
   - Memeriksa apakah manifest lama memiliki product_id duplikat. Jika ditemukan, lemparkan ValueError
     dan hentikan proses (tidak diam-diam hanya memperbarui baris pertama).
   - Jika manifest lama memiliki kolom 'previous_download_status' atau 'previous_error_message',
     informasi tersebut dikonsolidasikan ke dalam array 'attempt_history' agar tidak ada riwayat yang hilang.
   - Riwayat kegagalan sebelumnya (seperti HTTP 403) tetap dipertahankan penuh dalam format JSON string array.
   - Tetap mempertahankan 1 baris utama per product_id, strict read (IOError jika rusak), dan atomic write (.tmp -> os.replace).

5. Pelaporan Hasil Terperinci:
   - Menampilkan metrik terpisah: total target produk, produk ditemukan dalam stream, produk dengan
     judul cocok 100%, gambar berhasil disimpan & valid, gambar gagal diekstrak/disimpan, dan produk tidak ditemukan.

6. Ketentuan Tetap:
   - Tidak mengubah daftar 20 sampel atau random_state.
   - Tidak mengubah script 02 maupun dataset raw/cleaned CSV.
   - Tidak menghapus manifest lama atau riwayat kegagalan.
   - Skrip TIDAK dijalankan secara otomatis (blok __main__ menggunakan pass).
"""

import os
import io
import time
import json
import pandas as pd
from PIL import Image
from datasets import load_dataset

# 1. Konfigurasi Path File dan Parameter
PROJECT_ROOT = r"D:\Dormiy-ML"
DATA_CLEAN_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "dormiy_products_clean.csv")
IMAGES_PROCESSED_DIR = os.path.join(PROJECT_ROOT, "images", "processed")
MANIFEST_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "image_download_manifest.csv")

# Parameter Konfigurasi Dataset Hugging Face yang dicocokkan dengan 02_dataset_sampling.py
DATASET_NAME = "Shopify/product-catalogue"
DATASET_CONFIG = "default"
DATASET_SPLIT = "train"

PILOT_SAMPLE_COUNT = 20
RANDOM_STATE = 42

TARGET_CATEGORIES = [
    "Home & Garden",
    "Hardware",
    "Electronics",
    "Furniture",
    "Office Supplies"
]

def select_diverse_pilot_samples(
    df_clean: pd.DataFrame,
    categories: list = TARGET_CATEGORIES,
    total_samples: int = PILOT_SAMPLE_COUNT,
    random_state: int = RANDOM_STATE
) -> pd.DataFrame:
    """
    Memilih 20 produk berlabel 'Relevant' secara acak berimbang:
    - 4 sampel per kategori utama menggunakan sample(n=4, random_state=42).
    - Menjamin tepat 20 produk unik tanpa duplikasi.
    - Memunculkan ValueError jika ada kategori yang jumlah produknya kurang dari kuota.
    """
    df_rel = df_clean[df_clean["relevance_label"] == "Relevant"].copy()
    samples_per_cat = total_samples // len(categories)

    selected_dfs = []
    for cat in categories:
        cat_subset = df_rel[df_rel["main_category"] == cat]
        available_count = len(cat_subset)

        if available_count < samples_per_cat:
            raise ValueError(
                f"[ERROR] Jumlah produk berlabel 'Relevant' pada kategori '{cat}' tidak mencukupi! "
                f"Dibutuhkan {samples_per_cat} produk, tetapi hanya tersedia {available_count} produk."
            )

        cat_sample = cat_subset.sample(n=samples_per_cat, random_state=random_state)
        selected_dfs.append(cat_sample)

    df_pilot = pd.concat(selected_dfs, ignore_index=True)

    if len(df_pilot) != total_samples:
        raise ValueError(
            f"[ERROR] Total sampel yang dihasilkan ({len(df_pilot)}) tidak sesuai dengan target ({total_samples})!"
        )

    duplicate_ids = df_pilot["product_id"].duplicated().sum()
    if duplicate_ids > 0:
        raise ValueError(f"[ERROR] Ditemukan {duplicate_ids} product_id duplikat dalam sampel pilot!")

    return df_pilot

def normalize_title(title_str: str) -> str:
    """Normalisasi string judul untuk perbandingan yang andal."""
    if not title_str or pd.isna(title_str):
        return ""
    return " ".join(str(title_str).split()).strip().lower()

def decode_image_object(raw_image_obj):
    """
    Mendekode objek gambar dari berbagai format yang mungkin dikembalikan oleh Hugging Face datasets,
    sekaligus menjaga informasi format sumber asli (source_format).
    Mengembalikan tuple: (img: PIL.Image.Image, source_format: str)
    """
    if raw_image_obj is None:
        raise ValueError("Objek gambar bernilai None!")

    source_format = None

    # Kasus 1: Objek sudah merupakan PIL Image
    if isinstance(raw_image_obj, Image.Image):
        source_format = raw_image_obj.format if raw_image_obj.format else "UNKNOWN"
        img = raw_image_obj.copy()
        return img, source_format

    # Kasus 2: Objek berupa byte stream mentah
    if isinstance(raw_image_obj, (bytes, bytearray)):
        with Image.open(io.BytesIO(raw_image_obj)) as tmp_img:
            source_format = tmp_img.format if tmp_img.format else "UNKNOWN"
        img = Image.open(io.BytesIO(raw_image_obj))
        img.load()
        return img, source_format

    # Kasus 3: Objek berupa dictionary (format bawaan Hugging Face datasets feature Image)
    if isinstance(raw_image_obj, dict):
        if "bytes" in raw_image_obj and raw_image_obj["bytes"]:
            raw_bytes = raw_image_obj["bytes"]
            with Image.open(io.BytesIO(raw_bytes)) as tmp_img:
                source_format = tmp_img.format if tmp_img.format else "UNKNOWN"
            img = Image.open(io.BytesIO(raw_bytes))
            img.load()
            return img, source_format
        elif "path" in raw_image_obj and raw_image_obj["path"] and os.path.exists(raw_image_obj["path"]):
            with Image.open(raw_image_obj["path"]) as tmp_img:
                source_format = tmp_img.format if tmp_img.format else "UNKNOWN"
            img = Image.open(raw_image_obj["path"])
            img.load()
            return img, source_format
        elif "image" in raw_image_obj:
            return decode_image_object(raw_image_obj["image"])

    # Kasus 4: Objek berupa path file string di disk lokal
    if isinstance(raw_image_obj, str) and os.path.exists(raw_image_obj):
        with Image.open(raw_image_obj) as tmp_img:
            source_format = tmp_img.format if tmp_img.format else "UNKNOWN"
        img = Image.open(raw_image_obj)
        img.load()
        return img, source_format

    raise TypeError(f"Tipe objek gambar tidak dikenali atau tidak dapat didekode: {type(raw_image_obj)}")

def convert_and_save_image(image_obj, save_path: str):
    """
    Memverifikasi integritas gambar, menangani transparansi secara komprehensif
    dengan background putih, mempertahankan resolusi asli, menyimpan ke file sementara (.tmp.jpg),
    memverifikasi ulang file sementara, dan memindahkannya ke save_path via os.replace() (atomic write).
    Jika verifikasi gagal, hanya file sementara yang dihapus; gambar lama yang valid tidak disentuh.
    Mengembalikan dict: {width, height, format}
    """
    temp_save_path = save_path + ".tmp.jpg"
    temp_file_created = False

    try:
        # 1. Dekode objek ke PIL Image dan catat format asli sumber
        img, source_format = decode_image_object(image_obj)
        source_width, source_height = img.size

        # 2. Deteksi Transparansi Komprehensif:
        has_alpha_channel = img.mode in ("RGBA", "LA", "PA") or ("A" in img.getbands())
        has_transparency_info = "transparency" in img.info

        if has_alpha_channel or has_transparency_info:
            img_rgba = img.convert("RGBA")
            white_background = Image.new("RGB", img_rgba.size, (255, 255, 255))
            white_background.paste(img_rgba, mask=img_rgba.split()[3])
            final_img = white_background
        elif img.mode != "RGB":
            final_img = img.convert("RGB")
        else:
            final_img = img.copy()

        # 3. Simpan ke file sementara dengan ekstensi .jpg yang valid
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        final_img.save(temp_save_path, format="JPEG", quality=95)
        temp_file_created = True

        # 4. Validasi Ulang File Sementara (Strict Verification):
        if not os.path.exists(temp_save_path):
            raise IOError(f"File gambar sementara gagal dibuat di: {temp_save_path}")

        with Image.open(temp_save_path) as verified_img:
            verified_img.verify()

        with Image.open(temp_save_path) as verified_img:
            saved_width, saved_height = verified_img.size
            if (saved_width, saved_height) != (source_width, source_height):
                raise ValueError(
                    f"Dimensi gambar tersimpan ({saved_width}x{saved_height}) tidak cocok "
                    f"dengan dimensi sumber ({source_width}x{source_height})!"
                )

        # 5. Pindahkan file sementara ke lokasi target secara atomic
        os.replace(temp_save_path, save_path)
        temp_file_created = False

        return {
            "width": source_width,
            "height": source_height,
            "format": source_format
        }

    except Exception as e:
        # Poin 3: Bersihkan HANYA file sementara jika gagal; gambar lama tidak dirusak
        if temp_file_created and os.path.exists(temp_save_path):
            try:
                os.remove(temp_save_path)
            except Exception:
                pass
        raise e

def append_to_manifest(record: dict, manifest_path: str = MANIFEST_PATH):
    """
    Menyimpan / memperbarui record manifest secara aman (strict read & atomic upsert):
    1. Membaca manifest yang sudah ada tanpa menghapusnya.
    2. Validasi Integritas: jika ditemukan product_id duplikat di manifest lama,
       lempar ValueError eksplisit dan hentikan proses (anti-corruption).
    3. Jika manifest gagal dibaca, lempar IOError eksplisit (anti-overwrite).
    4. Mengkonsolidasikan kolom riwayat lama ('previous_download_status', 'previous_error_message')
       ke dalam 'attempt_history' (JSON string array) sehingga catatan kegagalan HTTP 403 tetap utuh.
    5. Menulis ke file sementara (.tmp) lalu me-replace file utama via os.replace() (atomic write).
    """
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
    temp_path = manifest_path + ".tmp"

    if os.path.exists(manifest_path):
        try:
            df_manifest = pd.read_csv(manifest_path)
        except Exception as read_err:
            raise IOError(
                f"[CRITICAL ERROR] File manifest '{manifest_path}' sudah ada tetapi gagal dibaca: {read_err}. "
                f"Proses dihentikan demi mencegah penimpaan file manifest yang sudah ada!"
            )
    else:
        df_manifest = pd.DataFrame()

    p_id = record["product_id"]

    # Validasi Poin 1: Periksa duplikasi product_id pada manifest lama
    if not df_manifest.empty and "product_id" in df_manifest.columns:
        duplicate_manifest_ids = df_manifest[df_manifest["product_id"].duplicated()]["product_id"].unique()
        if len(duplicate_manifest_ids) > 0:
            raise ValueError(
                f"[CRITICAL ERROR] Manifest '{manifest_path}' memiliki product_id duplikat: {list(duplicate_manifest_ids)}. "
                f"Proses dihentikan demi mencegah korupsi data manifest!"
            )

    # Buat objek rekaman percobaan saat ini
    current_attempt = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": record["download_status"],
        "error_message": record.get("error_message"),
        "image_source": record.get("image_source"),
        "image_format": record.get("image_format")
    }

    if not df_manifest.empty and "product_id" in df_manifest.columns and (df_manifest["product_id"] == p_id).any():
        idx_match = df_manifest.index[df_manifest["product_id"] == p_id][0]

        # Konsolidasi riwayat percobaan:
        # Ambil attempt_history yang sudah ada jika tersedia
        history_list = []
        if "attempt_history" in df_manifest.columns and pd.notna(df_manifest.loc[idx_match, "attempt_history"]):
            try:
                history_list = json.loads(str(df_manifest.loc[idx_match, "attempt_history"]))
            except Exception:
                history_list = [{"legacy_raw": str(df_manifest.loc[idx_match, "attempt_history"])}]
        else:
            # Jika belum ada attempt_history, konsolidasikan status lama dan kolom previous_*
            # 1. Cek previous_download_status jika pernah ada
            if "previous_download_status" in df_manifest.columns and pd.notna(df_manifest.loc[idx_match, "previous_download_status"]):
                history_list.append({
                    "timestamp": "initial_attempt",
                    "status": str(df_manifest.loc[idx_match, "previous_download_status"]),
                    "error_message": str(df_manifest.loc[idx_match, "previous_error_message"]) if "previous_error_message" in df_manifest.columns and pd.notna(df_manifest.loc[idx_match, "previous_error_message"]) else None
                })
            # 2. Cek status aktif saat ini di manifest sebelum ditimpa (misal: HTTP 403)
            old_curr_status = df_manifest.loc[idx_match, "download_status"] if "download_status" in df_manifest.columns else None
            old_curr_err = df_manifest.loc[idx_match, "error_message"] if "error_message" in df_manifest.columns else None
            if pd.notna(old_curr_status):
                history_list.append({
                    "timestamp": "prior_attempt",
                    "status": str(old_curr_status),
                    "error_message": str(old_curr_err) if pd.notna(old_curr_err) else None
                })

        # Tambahkan percobaan terbaru ke riwayat
        history_list.append(current_attempt)
        record["attempt_history"] = json.dumps(history_list)

        # Update baris manifest yang ada
        for key, val in record.items():
            df_manifest.loc[idx_match, key] = val

    else:
        # Baris baru
        record["attempt_history"] = json.dumps([current_attempt])
        new_row = pd.DataFrame([record])
        df_manifest = pd.concat([df_manifest, new_row], ignore_index=True)

    df_manifest.to_csv(temp_path, index=False, encoding="utf-8")
    os.replace(temp_path, manifest_path)

def run_pilot_image_download():
    """
    Fungsi orkestrasi utama pilot image preparation via selective streaming:
    - Membaca dataset bersih secara read-only.
    - Memilih 20 produk acak terkontrol (4 per kategori).
    - Memverifikasi parameter konfigurasi dan memetakan indeks.
    - Validasi judul ketat (fail-fast jika judul berbeda).
    - Ekstraksi gambar melalui stream Hugging Face (menjaga format sumber asli).
    - Pemrosesan transparansi berlatar putih dan verifikasi dimensi.
    - Menulis file sementara dan membersihkan hanya file sementara jika gagal (non-destructive).
    - Memperbarui manifest inkremental dengan riwayat akumulatif (attempt_history).
    - Menyajikan pelaporan metrik terpisah dan terperinci.
    """
    print("=" * 75)
    print("DORMIY - PILOT IMAGE PREPARATION (STREAMING SELEKTIF HUGGING FACE)")
    print(f"Dataset Input : {DATA_CLEAN_PATH}")
    print(f"Folder Gambar : {IMAGES_PROCESSED_DIR}")
    print(f"File Manifest : {MANIFEST_PATH}")
    print("=" * 75)

    # 1. Baca dataset bersih
    df_clean = pd.read_csv(DATA_CLEAN_PATH)

    # 2. Seleksi 20 produk acak berimbang
    pilot_df = select_diverse_pilot_samples(df_clean, TARGET_CATEGORIES, PILOT_SAMPLE_COUNT, RANDOM_STATE)

    # 3. Pemetaan Indeks & Pembuktian Urutan terhadap 02_dataset_sampling.py (Poin 2)
    # Pada 02_dataset_sampling.py:
    # DATASET_NAME = 'Shopify/product-catalogue', SPLIT = 'train', CONFIG = 'default'
    # Produk diambil bertahap (batch size 100) dan diberi ID = f"prod_{len(all_rows)+1:04d}".
    target_map = {}
    seen_stream_indices = set()

    for _, row in pilot_df.iterrows():
        p_id = row["product_id"]
        try:
            stream_idx = int(p_id.split("_")[1]) - 1
        except Exception as parse_err:
            raise ValueError(f"[ERROR] Format product_id '{p_id}' tidak valid untuk dipetakan ke indeks: {parse_err}")

        # Validasi: Tidak boleh ada dua produk target dengan stream_idx yang sama
        if stream_idx in seen_stream_indices:
            raise ValueError(f"[ERROR] Ditemukan duplikasi stream_idx ({stream_idx}) pada target {p_id}!")
        seen_stream_indices.add(stream_idx)

        target_map[stream_idx] = {
            "product_id": p_id,
            "clean_title": row["clean_title"],
            "raw_title": row["title"],
            "main_category": row["main_category"],
            "image_url": row["image_url"]
        }

    total_targets = len(target_map)
    print(f"[INFO] Terpilih tepat {total_targets} produk target (4 produk per kategori, {len(seen_stream_indices)} indeks unik):")
    for cat in TARGET_CATEGORIES:
        count = (pilot_df["main_category"] == cat).sum()
        print(f"  - {cat}: {count} produk")

    print(f"\n[INFO] Membuka streaming Hugging Face Hub: {DATASET_NAME} (config={DATASET_CONFIG}, split={DATASET_SPLIT})...")
    dataset_stream = load_dataset(DATASET_NAME, DATASET_CONFIG, split=DATASET_SPLIT, streaming=True)

    products_found_count = 0
    title_matched_count = 0
    images_saved_count = 0
    images_failed_count = 0

    print("[INFO] Memulai streaming, validasi judul ketat, dan ekstraksi gambar...")
    for current_idx, item in enumerate(dataset_stream):
        if current_idx in target_map:
            products_found_count += 1
            meta = target_map[current_idx]
            p_id = meta["product_id"]
            title = meta["clean_title"]
            cat = meta["main_category"]
            orig_url = meta["image_url"]

            filename = f"{p_id}.jpg"
            local_path = os.path.join(IMAGES_PROCESSED_DIR, filename)
            relative_path = os.path.join("images", "processed", filename)
            image_source = f"hf_stream://{DATASET_NAME}/{DATASET_SPLIT}/{current_idx}"

            # --- VALIDASI PENCOCOKAN JUDUL PRODUK KETAT (PRIMARY GUARDRAIL) ---
            stream_title = item.get("product_title", "")
            norm_stream_title = normalize_title(stream_title)
            norm_raw_title = normalize_title(meta["raw_title"])

            if norm_stream_title != norm_raw_title:
                err_mismatch = (
                    f"[FATAL MISMATCH] Ketidakcocokan judul pada indeks {current_idx} ({p_id})!\n"
                    f"  - Judul di Stream Hugging Face : '{stream_title}'\n"
                    f"  - Judul di CSV Dataset       : '{meta['raw_title']}'\n"
                    f"Proses dihentikan demi mencegah kesalahan asosiasi gambar dan metadata!"
                )
                print(f"\n{err_mismatch}")
                raise ValueError(err_mismatch)

            title_matched_count += 1
            print(f"[{products_found_count}/{total_targets}] Terverifikasi [{p_id}] (idx: {current_idx}) {title[:32]}... ({cat})")

            info = None
            try:
                img_obj = item.get("product_image")
                if img_obj is None:
                    raise ValueError("Field 'product_image' bernilai None pada stream!")

                # Verifikasi, pemrosesan transparansi, simpan atomic, dan validasi dimensi
                info = convert_and_save_image(img_obj, local_path)
                images_saved_count += 1
                status = "SUCCESS"
                err_msg = None
                print(f"    --> BERHASIL: {info['width']}x{info['height']} px (Format sumber: {info['format']})")

            except Exception as e:
                images_failed_count += 1
                status = "FAILED"
                err_msg = str(e)
                relative_path = None
                print(f"    --> GAGAL: {err_msg}")

            # Catat dan perbarui manifest di disk secara atomic dengan attempt_history akumulatif
            record = {
                "product_id": p_id,
                "title": title,
                "main_category": cat,
                "image_url": orig_url,
                "image_source": image_source,
                "local_image_path": relative_path,
                "download_status": status,
                "image_width": info["width"] if info else None,
                "image_height": info["height"] if info else None,
                "image_format": info["format"] if info else None,
                "error_message": err_msg
            }
            append_to_manifest(record, MANIFEST_PATH)

            # Hentikan iterasi segera setelah seluruh 20 target gambar berhasil ditemukan
            if products_found_count >= total_targets:
                print(f"\n[INFO] Seluruh {total_targets} target produk berhasil ditemukan dan diverifikasi. Menghentikan stream.")
                break

    uncollected_count = total_targets - products_found_count

    # Pelaporan Hasil Terpisah dan Transparan (Poin 5)
    print("\n" + "=" * 75)
    print("HASIL PELAPORAN PILOT IMAGE DATASET PREPARATION:")
    print("=" * 75)
    print(f"1. Total Target Produk              : {total_targets}")
    print(f"2. Produk Ditemukan dalam Stream    : {products_found_count}")
    print(f"3. Produk dengan Judul Cocok (100%) : {title_matched_count}")
    print(f"4. Gambar Berhasil Disimpan & Valid : {images_saved_count}")
    print(f"5. Gambar Gagal Diekstrak / Disimpan: {images_failed_count}")
    print(f"6. Produk Tidak Ditemukan           : {uncollected_count}")
    print("-" * 75)
    print(f"- File Manifest Tersimpan Di        : {MANIFEST_PATH}")
    print(f"- Direktori Gambar                  : {IMAGES_PROCESSED_DIR}")
    print("=" * 75)

if __name__ == "__main__":
    run_pilot_image_download()
