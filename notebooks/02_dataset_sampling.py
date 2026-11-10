"""
Skrip 02: Initial Dataset Sampling (Metadata Only) - Proyek DORMIY
Tujuan:
- Mengambil maksimal 1.000 produk dari split 'train' dataset Shopify/product-catalogue.
- Mengambil metadata teks saja (tanpa mengunduh file gambar biner secara massal).
- Menyimpan ke: data/raw/shopify_sample_1000.csv dengan encoding UTF-8.
- Dilengkapi mekanisme retry untuk mengatasi fluktuasi jaringan/timeout.
- Memeriksa missing values pada kolom metadata dan menampilkan 10 contoh sampel produk.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
import pandas as pd

# Konfigurasi Parameter
DATASET_NAME = "Shopify/product-catalogue"
SPLIT = "train"
CONFIG = "default"
TARGET_SAMPLES = 1000
BATCH_SIZE = 100  # Batas per request ke HF rows API

# Konfigurasi Path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "shopify_sample_1000.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_batch_with_retry(offset: int, length: int, max_retries: int = 5, backoff_factor: int = 2):
    """
    Mengambil batch metadata menggunakan Hugging Face Datasets Server API.
    Metode ini sangat efisien karena server HF mengembalikan URL gambar (bukan raw bytes gambar),
    sehingga hemat bandwidth dan menghindari timeout handshake SSL parquet besar.
    """
    url = f"https://datasets-server.huggingface.co/rows?dataset={DATASET_NAME}&config={CONFIG}&split={SPLIT}&offset={offset}&limit={length}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "DORMIY-Dataset-Sampling/1.0 (Machine Learning Project)"}
    )

    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("rows", [])
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionResetError) as err:
            wait_time = backoff_factor ** attempt
            print(f"[RETRY {attempt}/{max_retries}] Kendala jaringan pada offset {offset}: {err}. Menunggu {wait_time} detik...")
            time.sleep(wait_time)
            if attempt == max_retries:
                raise RuntimeError(f"Gagal mengambil batch pada offset {offset} setelah {max_retries} percobaan: {err}")

def run_sampling():
    print("=" * 60)
    print("DORMIY - INITIAL DATASET SAMPLING (METADATA ONLY)")
    print(f"Dataset : {DATASET_NAME} | Split: {SPLIT}")
    print(f"Target  : {TARGET_SAMPLES} baris produk")
    print(f"Output  : {OUTPUT_CSV}")
    print("=" * 60)

    all_rows = []
    offset = 0

    while len(all_rows) < TARGET_SAMPLES:
        batch_limit = min(BATCH_SIZE, TARGET_SAMPLES - len(all_rows))
        print(f"[FETCHING] Mengambil offset {offset} sampai {offset + batch_limit}...")
        
        try:
            rows = fetch_batch_with_retry(offset, batch_limit)
        except Exception as e:
            print(f"[ERROR] {e}")
            break

        if not rows:
            print("[INFO] Tidak ada data lagi yang diterima dari server.")
            break

        for item in rows:
            row_data = item.get("row", {})
            
            # Ekstraksi metadata produk
            title = row_data.get("product_title")
            desc = row_data.get("product_description")
            category = row_data.get("ground_truth_category")
            brand = row_data.get("ground_truth_brand")
            is_secondhand = row_data.get("ground_truth_is_secondhand")
            potential_cats = row_data.get("potential_product_categories")
            
            # Ekstraksi URL / status gambar tanpa mendownload biner gambar
            image_info = row_data.get("product_image")
            image_url = None
            has_image = False
            if isinstance(image_info, dict):
                image_url = image_info.get("src")
                has_image = bool(image_url)
            elif image_info is not None:
                has_image = True

            all_rows.append({
                "product_id": f"prod_{len(all_rows)+1:04d}",
                "title": title,
                "description": desc,
                "category": category,
                "brand": brand,
                "is_secondhand": is_secondhand,
                "potential_categories": json.dumps(potential_cats) if potential_cats is not None else None,
                "has_image": has_image,
                "image_url": image_url
            })

        offset += len(rows)
        print(f"[PROGRESS] Terkumpul: {len(all_rows)} / {TARGET_SAMPLES} data.")

    # 1. Simpan ke DataFrame dan file CSV
    df = pd.DataFrame(all_rows)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\n[SUKSES] {len(df)} baris data berhasil disimpan ke: {OUTPUT_CSV}")

    # 2. Pemeriksaan Missing Values
    print("\n" + "=" * 60)
    print("ANALISIS MISSING VALUES (PADA 1.000 SAMPEL RAW)")
    print("=" * 60)
    missing_summary = pd.DataFrame({
        "Jumlah Missing": df.isnull().sum(),
        "Persentase (%)": (df.isnull().sum() / len(df) * 100).round(2)
    })
    print(missing_summary.to_string())

    # 3. Tampilkan 10 Contoh Sampel Produk Pertama
    print("\n" + "=" * 60)
    print("10 CONTOH SAMPEL PRODUK AWAL")
    print("=" * 60)
    for idx in range(min(10, len(df))):
        sample = df.iloc[idx]
        print(f"\n[Produk {idx+1}] ID: {sample['product_id']}")
        print(f"  Judul     : {sample['title']}")
        desc_preview = str(sample['description'])[:90] + "..." if pd.notna(sample['description']) else "<KOSONG / NaN>"
        print(f"  Deskripsi : {desc_preview}")
        print(f"  Kategori  : {sample['category']}")
        print(f"  Brand     : {sample['brand']}")
        print(f"  Gambar    : {'Tersedia (URL terlampir)' if sample['has_image'] else 'Tidak Tersedia'}")

if __name__ == "__main__":
    run_sampling()

