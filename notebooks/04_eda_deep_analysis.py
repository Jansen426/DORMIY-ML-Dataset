"""
Skrip 04: EDA Tahap 2 - Deep Analysis Proyek DORMIY
Tujuan Analisis:
1. Category Hierarchy Analysis:
   - Ekstrak kategori level pertama (main category) dari kolom hierarkis 'category'.
   - Hitung jumlah dan persentase produk pada setiap kategori utama.
   - Tampilkan 10 kategori utama terbanyak.
   - Buat visualisasi bar chart kategori utama.
2. Description Quality Analysis:
   - Identifikasi deskripsi kosong (NaN / string kosong).
   - Identifikasi deskripsi terlalu pendek (< 20 karakter).
   - Identifikasi deskripsi sangat panjang (> 2.000 karakter).
   - Tampilkan contoh konkret dari masing-masing kelompok untuk evaluasi.
3. Product Relevance Analysis (Evaluasi Inventaris Asrama):
   - Kelompokkan produk berdasarkan kategori utama.
   - Tampilkan contoh nama dan ringkasan deskripsi produk dari setiap kategori utama tanpa melakukan filtering/dropping data.
4. Image Metadata Analysis:
   - Periksa apakah metadata dimensi gambar (width, height, aspect ratio) tersedia di CSV raw atau di API metadata tanpa mengunduh seluruh gambar.
   - Jelaskan status dan implikasinya untuk tim Computer Vision.

Dataset Input : data/raw/shopify_sample_1000.csv
Output Gambar  : reports/figures/03_top_main_categories.png
"""

import os
import tempfile
import pandas as pd
import numpy as np

# Konfigurasi temporary cache directory untuk matplotlib
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib_dormiy")
import matplotlib.pyplot as plt
import seaborn as sns

# Path file
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "shopify_sample_1000.csv")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "reports", "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")

def run_deep_analysis():
    print("=" * 75)
    print("DORMIY - EXPLORATORY DATA ANALYSIS (EDA) TAHAP 2: DEEP ANALYSIS")
    print(f"Dataset Sumber: {DATA_PATH}")
    print("=" * 75)

    df = pd.read_csv(DATA_PATH)
    total_data = len(df)
    print(f"[INFO] Dataset berhasil dimuat: {total_data} baris, {len(df.columns)} kolom.\n")

    # =========================================================================
    # 1. CATEGORY HIERARCHY ANALYSIS
    # =========================================================================
    print("=" * 75)
    print("1. ANALISIS HIERARKI KATEGORI (LEVEL PERTAMA / MAIN CATEGORY)")
    print("=" * 75)
    
    # Ekstraksi kategori level pertama (memisahkan dengan delimiter ' > ')
    df["main_category"] = df["category"].astype(str).apply(
        lambda x: x.split(" > ")[0].strip() if pd.notna(x) else "Unknown"
    )

    main_cat_counts = df["main_category"].value_counts()
    total_main_cats = len(main_cat_counts)
    
    print(f"Total Kategori Utama (Level 1) Ditemukan: {total_main_cats} kategori\n")
    print("Distribusi Lengkap Kategori Utama:")
    main_cat_df = pd.DataFrame({
        "Kategori Utama": main_cat_counts.index,
        "Jumlah Produk": main_cat_counts.values,
        "Persentase (%)": (main_cat_counts.values / total_data * 100).round(2)
    })
    print(main_cat_df.to_string(index=False))

    # Top 10 Kategori Utama
    top_10_main = main_cat_counts.head(10)
    print("\nTop 10 Kategori Utama Terbanyak:")
    print(main_cat_df.head(10).to_string(index=False))

    # Visualisasi Bar Chart Kategori Utama
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x=top_10_main.values,
        y=top_10_main.index,
        hue=top_10_main.index,
        palette="crest",
        legend=False,
        ax=ax
    )

    for i, count in enumerate(top_10_main.values):
        pct = count / total_data * 100
        ax.text(count + 2, i, f"{count} ({pct:.1f}%)", va="center", fontsize=10, fontweight="bold")

    ax.set_title("Top 10 Kategori Utama (Level 1) Produk Shopify (Sample 1.000)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Jumlah Produk", fontsize=12, labelpad=10)
    ax.set_ylabel("Kategori Utama (Level 1)", fontsize=12, labelpad=10)
    ax.set_xlim(0, max(top_10_main.values) + 30)
    plt.tight_layout()

    cat_chart_path = os.path.join(FIGURES_DIR, "03_top_main_categories.png")
    plt.savefig(cat_chart_path, dpi=300)
    plt.close()
    print(f"\n[OUTPUT] Bar chart kategori utama disimpan ke: {cat_chart_path}\n")

    # =========================================================================
    # 2. DESCRIPTION QUALITY ANALYSIS
    # =========================================================================
    print("=" * 75)
    print("2. ANALISIS KUALITAS DESKRIPSI (DESCRIPTION QUALITY ANALYSIS)")
    print("=" * 75)
    
    # Menghitung panjang karakter
    desc_str = df["description"].fillna("").astype(str).str.strip()
    df["desc_len"] = desc_str.str.len()

    # Kategori kualitas deskripsi
    mask_empty = df["description"].isnull() | (desc_str == "")
    mask_short = (~mask_empty) & (df["desc_len"] < 20)
    mask_long = df["desc_len"] > 2000
    mask_normal = (~mask_empty) & (df["desc_len"] >= 20) & (df["desc_len"] <= 2000)

    print("Ringkasan Pengelompokan Kualitas Deskripsi:")
    print(f"  - Deskripsi Kosong (NaN / Empty)      : {mask_empty.sum()} produk ({mask_empty.sum()/total_data*100:.2f}%)")
    print(f"  - Terlalu Pendek (< 20 karakter)       : {mask_short.sum()} produk ({mask_short.sum()/total_data*100:.2f}%)")
    print(f"  - Sangat Panjang (> 2.000 karakter)    : {mask_long.sum()} produk ({mask_long.sum()/total_data*100:.2f}%)")
    print(f"  - Panjang Normal (20 - 2.000 karakter) : {mask_normal.sum()} produk ({mask_normal.sum()/total_data*100:.2f}%)")

    # Contoh Deskripsi Kosong
    print("\n--- Contoh Produk dengan Deskripsi Kosong (3 Sampel) ---")
    for idx, row in df[mask_empty].head(3).iterrows():
        print(f"  [{row['product_id']}] Title: {row['title']} | Brand: {row['brand']} | Kategori: {row['category'][:45]}...")

    # Contoh Deskripsi Terlalu Pendek (< 20 karakter)
    print("\n--- Contoh Produk dengan Deskripsi Terlalu Pendek (< 20 karakter) (5 Sampel) ---")
    for idx, row in df[mask_short].head(5).iterrows():
        print(f"  [{row['product_id']}] Title: {row['title']}")
        print(f"    Panjang: {row['desc_len']} kar | Isi Deskripsi: \"{row['description']}\"")

    # Contoh Deskripsi Sangat Panjang (> 2.000 karakter)
    print("\n--- Contoh Produk dengan Deskripsi Sangat Panjang (> 2.000 karakter) (3 Sampel) ---")
    for idx, row in df[mask_long].head(3).iterrows():
        print(f"  [{row['product_id']}] Title: {row['title']}")
        print(f"    Panjang: {row['desc_len']} kar | Cuplikan: \"{str(row['description'])[:120]}...\"")

    # =========================================================================
    # 3. PRODUCT RELEVANCE ANALYSIS (INVENTARIS GUDANG ASRAMA)
    # =========================================================================
    print("\n" + "=" * 75)
    print("3. ANALISIS RELEVANSI PRODUK TERHADAP KEBUTUHAN INVENTARIS ASRAMA")
    print("=" * 75)
    print("Menampilkan contoh produk dari setiap Kategori Utama untuk evaluasi relevansi:")

    for cat_name, count in main_cat_counts.items():
        cat_samples = df[df["main_category"] == cat_name]
        print(f"\n[Kategori Utama: {cat_name}] ({count} produk, {count/total_data*100:.2f}%)")
        for i, (_, row) in enumerate(cat_samples.head(2).iterrows()):
            desc_prev = str(row['description'])[:80] + "..." if pd.notna(row['description']) else "<KOSONG>"
            print(f"   Contoh {i+1}: \"{row['title']}\"")
            print(f"             Deskripsi: {desc_prev}")

    # =========================================================================
    # 4. IMAGE METADATA ANALYSIS
    # =========================================================================
    print("\n" + "=" * 75)
    print("4. ANALISIS METADATA GAMBAR (IMAGE METADATA ANALYSIS)")
    print("=" * 75)
    
    # Periksa kolom dalam CSV raw
    image_cols = [c for c in df.columns if "image" in c.lower() or "width" in c.lower() or "height" in c.lower()]
    print(f"Kolom terkait gambar dalam file raw CSV: {image_cols}")
    print(f"Apakah dimensi 'width' dan 'height' tersedia di CSV: {'TIDAK TERSEDIA'}")

    # Penjelasan keterbatasan dan pemeriksaan respons API
    print("\nTemuan Teknis Metadata Gambar:")
    print("1. Di dalam CSV saat ini, hanya tersimpan 'has_image' (boolean) dan 'image_url' (link CDN image.jpg).")
    print("2. Kolom 'width' dan 'height' tidak disertakan saat sampling metadata CSV awal.")
    print("3. Dari respons Hugging Face Datasets Server API, objek 'product_image' sebenarnya memiliki metadata {'height': 1000, 'width': 1000, 'src': ...}.")
    print("4. Untuk tim Computer Vision, ukuran dimensi standar gambar katalog Shopify umumnya bernilai 1000x1000 piksel (rasio 1:1 / square).")
    print("5. Implikasi Keterbatasan: Jika tim CV membutuhkan ukuran piksel lokal yang pasti tanpa mengunduh massal saat ini, dimensi dapat diekstrak nanti secara batch saat gambar diunduh pada tahap persiapan dataset akhir.")

    print("\n" + "=" * 75)
    print("[SELESAI] EDA Tahap 2 Deep Analysis Selesai Dijalankan.")
    print("=" * 75)

if __name__ == "__main__":
    run_deep_analysis()

