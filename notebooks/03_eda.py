"""
Skrip 03: Exploratory Data Analysis (EDA) - Proyek DORMIY
Tujuan:
1. Category Distribution:
   - Hitung jumlah produk per kategori.
   - Tampilkan 10 kategori terbanyak.
   - Buat bar chart visualisasi 10 kategori terbanyak.
2. Description Length Analysis:
   - Hitung panjang karakter setiap deskripsi produk.
   - Tampilkan statistik deskriptif: mean, median, min, max.
   - Buat visualisasi histogram distribusi panjang deskripsi.
3. Text-Image Completeness:
   - Hitung jumlah & persentase kelengkapan pasangan teks (title & description) dan gambar.
4. Data Quality Overview:
   - Hitung missing values pada setiap kolom.
   - Periksa duplikasi data berdasarkan 'title'.

Dataset Input: data/raw/shopify_sample_1000.csv
Output Gambar : reports/figures/
"""

import os
import tempfile
import pandas as pd
import numpy as np

# Konfigurasi direktori cache matplotlib agar stabil di Windows
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib_dormiy")
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Path File
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "shopify_sample_1000.csv")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "reports", "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)

# Set style seaborn untuk visualisasi yang rapi dan profesional
sns.set_theme(style="whitegrid")

def run_eda():
    print("=" * 70)
    print("DORMIY - EXPLORATORY DATA ANALYSIS (EDA) TAHAP 1")
    print(f"Dataset Sumber: {DATA_PATH}")
    print(f"Output Grafik : {FIGURES_DIR}")
    print("=" * 70)

    # Membaca dataset raw
    df = pd.read_csv(DATA_PATH)
    total_data = len(df)
    print(f"[INFO] Dataset berhasil dimuat: {total_data} baris, {len(df.columns)} kolom.\n")

    # =========================================================================
    # 1. CATEGORY DISTRIBUTION
    # =========================================================================
    print("-" * 70)
    print("1. ANALISIS DISTRIBUSI KATEGORI PRODUK")
    print("-" * 70)
    category_counts = df["category"].value_counts()
    total_categories = len(category_counts)
    print(f"Total kategori unik dalam 1.000 sampel: {total_categories} kategori\n")
    
    top_10_categories = category_counts.head(10)
    print("Top 10 Kategori Produk Terbanyak:")
    top_10_df = pd.DataFrame({
        "Kategori": top_10_categories.index,
        "Jumlah Produk": top_10_categories.values,
        "Persentase (%)": (top_10_categories.values / total_data * 100).round(2)
    })
    print(top_10_df.to_string(index=False))

    # Visualisasi Bar Chart Top 10 Kategori
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Mempersingkat label kategori yang terlalu panjang untuk visualisasi yang rapi
    shortened_labels = [
        cat if len(cat) <= 45 else cat[:42] + "..." 
        for cat in top_10_categories.index
    ]
    
    sns.barplot(
        x=top_10_categories.values,
        y=shortened_labels,
        palette="viridis",
        ax=ax
    )
    
    # Tambahkan angka di ujung setiap batang bar
    for i, count in enumerate(top_10_categories.values):
        ax.text(count + 0.3, i, str(count), va="center", fontsize=10, fontweight="bold")

    ax.set_title("Top 10 Distribusi Kategori Produk (Shopify Sample 1.000)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Jumlah Produk", fontsize=12, labelpad=10)
    ax.set_ylabel("Kategori Produk", fontsize=12, labelpad=10)
    plt.tight_layout()
    
    cat_chart_path = os.path.join(FIGURES_DIR, "01_top_10_categories.png")
    plt.savefig(cat_chart_path, dpi=300)
    plt.close()
    print(f"\n[OUTPUT] Bar chart kategori disimpan ke: {cat_chart_path}\n")

    # =========================================================================
    # 2. DESCRIPTION LENGTH ANALYSIS
    # =========================================================================
    print("-" * 70)
    print("2. ANALISIS PANJANG KARAKTER DESKRIPSI")
    print("-" * 70)
    
    # Menghitung panjang karakter untuk setiap deskripsi
    # Produk dengan deskripsi NaN memiliki panjang karakter 0
    df["desc_length"] = df["description"].fillna("").astype(str).str.len()
    
    # Hitung statistik deskriptif
    desc_mean = df["desc_length"].mean()
    desc_median = df["desc_length"].median()
    desc_min = df["desc_length"].min()
    desc_max = df["desc_length"].max()
    desc_std = df["desc_length"].std()

    # Statistik khusus untuk deskripsi yang tidak kosong (> 0)
    non_zero_lengths = df[df["desc_length"] > 0]["desc_length"]
    
    print("Statistik Panjang Deskripsi (Seluruh 1.000 Produk):")
    print(f"  - Nilai Minimum (Min) : {desc_min} karakter")
    print(f"  - Nilai Rata-rata (Mean) : {desc_mean:.2f} karakter")
    print(f"  - Nilai Tengah (Median) : {desc_median:.2f} karakter")
    print(f"  - Nilai Maksimum (Max) : {desc_max} karakter")
    print(f"  - Standar Deviasi (Std): {desc_std:.2f} karakter")
    print(f"\nStatistik Khusus Produk yang Memiliki Deskripsi ({len(non_zero_lengths)} produk):")
    print(f"  - Nilai Minimum        : {non_zero_lengths.min()} karakter")
    print(f"  - Rata-rata (Mean)     : {non_zero_lengths.mean():.2f} karakter")
    print(f"  - Nilai Tengah (Median): {non_zero_lengths.median():.2f} karakter")
    print(f"  - Nilai Maksimum       : {non_zero_lengths.max()} karakter")

    # Visualisasi Histogram Distribusi Panjang Deskripsi
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Menggunakan representasi hingga persentil 98 untuk menghindari outlier ekstrem pada visual
    cutoff = df["desc_length"].quantile(0.98)
    filtered_lengths = df[df["desc_length"] <= cutoff]["desc_length"]

    sns.histplot(
        filtered_lengths,
        bins=40,
        kde=True,
        color="#2b5c8f",
        edgecolor="black",
        ax=ax
    )

    ax.axvline(desc_mean, color="red", linestyle="--", linewidth=1.8, label=f"Mean: {desc_mean:.1f}")
    ax.axvline(desc_median, color="green", linestyle="-.", linewidth=1.8, label=f"Median: {desc_median:.1f}")

    ax.set_title("Distribusi Panjang Karakter Deskripsi Produk (Shopify Sample 1.000)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Panjang Karakter Deskripsi", fontsize=12, labelpad=10)
    ax.set_ylabel("Frekuensi / Jumlah Produk", fontsize=12, labelpad=10)
    ax.legend(fontsize=11)
    plt.tight_layout()

    desc_chart_path = os.path.join(FIGURES_DIR, "02_description_length_distribution.png")
    plt.savefig(desc_chart_path, dpi=300)
    plt.close()
    print(f"\n[OUTPUT] Histogram panjang deskripsi disimpan ke: {desc_chart_path}\n")

    # =========================================================================
    # 3. TEXT-IMAGE COMPLETENESS
    # =========================================================================
    print("-" * 70)
    print("3. KELENGKAPAN PASANGAN TEKS DAN GAMBAR (TEXT-IMAGE COMPLETENESS)")
    print("-" * 70)
    
    has_title = df["title"].notnull() & (df["title"].astype(str).str.strip() != "")
    has_desc = df["description"].notnull() & (df["description"].astype(str).str.strip() != "")
    has_image = df["has_image"] & df["image_url"].notnull()
    
    # Kondisi kelengkapan penuh (Multi-modal siap)
    complete_pair = has_title & has_desc & has_image
    
    completeness_summary = [
        {"Komponen": "Memiliki Judul (Title)", "Jumlah": has_title.sum(), "Persentase (%)": round(has_title.sum() / total_data * 100, 2)},
        {"Komponen": "Memiliki Deskripsi (Description)", "Jumlah": has_desc.sum(), "Persentase (%)": round(has_desc.sum() / total_data * 100, 2)},
        {"Komponen": "Memiliki URL Gambar (Image)", "Jumlah": has_image.sum(), "Persentase (%)": round(has_image.sum() / total_data * 100, 2)},
        {"Komponen": "Lengkap Penuh: Judul + Deskripsi + Gambar", "Jumlah": complete_pair.sum(), "Persentase (%)": round(complete_pair.sum() / total_data * 100, 2)},
        {"Komponen": "Tidak Lengkap (Missing salah satu/lebih)", "Jumlah": total_data - complete_pair.sum(), "Persentase (%)": round((total_data - complete_pair.sum()) / total_data * 100, 2)}
    ]
    
    completeness_df = pd.DataFrame(completeness_summary)
    print(completeness_df.to_string(index=False))

    # =========================================================================
    # 4. DATA QUALITY OVERVIEW
    # =========================================================================
    print("\n" + "-" * 70)
    print("4. IKHTISAR KUALITAS DATA (DATA QUALITY OVERVIEW)")
    print("-" * 70)
    
    # Missing values per kolom
    missing_series = df.isnull().sum()
    missing_df = pd.DataFrame({
        "Nama Kolom": missing_series.index,
        "Missing Values": missing_series.values,
        "Persentase (%)": (missing_series.values / total_data * 100).round(2)
    })
    print("Ikhtisar Missing Values per Kolom:")
    print(missing_df.to_string(index=False))
    
    # Duplikasi berdasarkan title
    title_duplicates = df.duplicated(subset=["title"]).sum()
    unique_titles = df["title"].nunique()
    print(f"\nAnalisis Duplikasi Kolom 'title':")
    print(f"  - Judul Unik               : {unique_titles}")
    print(f"  - Judul Duplikat Terdeteksi: {title_duplicates} baris ({title_duplicates / total_data * 100:.2f}%)")
    
    if title_duplicates > 0:
        print("\nContoh Judul yang Muncul Lebih dari Sekali:")
        dup_titles = df[df.duplicated(subset=["title"], keep=False)]["title"].value_counts().head(5)
        for t, c in dup_titles.items():
            print(f"  * \"{t}\" (muncul {c} kali)")

    print("\n" + "=" * 70)
    print("[SELESAI] Analisis EDA Tahap 1 Selesai Dijalankan Tanpa Mengubah Data Raw.")
    print("=" * 70)

if __name__ == "__main__":
    run_eda()

