# Laporan Verifikasi Final (Final Verification Report) - Proyek DORMIY

**Tanggal Verifikasi:** 10 November 2026  
**Task:** Dataset Preparation, Exploratory Data Analysis (EDA) & Data Cleaning  
**Target Tim:** Tim NLP (Farhan) dan Tim Computer Vision (Noel)  
**Metode:** Read-Only Audit & Strict Verification Testing  

---

## 1. Ringkasan Status Verifikasi (Dashboard)

| No | Komponen Verifikasi | Status | Ringkasan Hasil Pemeriksaan Aktual |
| :---: | :--- | :---: | :--- |
| **1** | **Validasi Manifest CV** | **PASS** | Tepat 50 record produk unik, 0 duplikasi, dan seluruh 50 berstatus `SUCCESS`. |
| **2** | **Validasi File Gambar** | **PASS** | Seluruh 50 file citra ada di `data/final/cv/images/`, 100% lolos verifikasi Pillow (`verify()`), 0 corrupt, format JPEG konsisten. |
| **3** | **Validasi Relasi Data** | **PASS (With Note)** | 43 gambar terhubung langsung dengan katalog kandidat `dormiy_nlp_catalog.csv`. 7 gambar berasal dari pilot yang berstatus `Excluded_NLP` (tersimpan di `dormiy_products_clean.csv`). |
| **4** | **Validasi Katalog NLP** | **PASS** | File CSV dan JSON memiliki tepat 337 baris identik atribut per atribut, 0 missing `text_for_nlp`, 0 duplikasi ID. |
| **5** | **Validasi Struktur Final** | **PASS** | Seluruh 5 direktori/file final tersedia, tidak kosong, dan memiliki ukuran valid. |

---

## 2. Rincian Hasil Pemeriksaan 5 Kriteria

### A. Pemeriksaan 1: Validasi Manifest Computer Vision
- **File Diperiksa:** [`data/final/cv/dormiy_cv_manifest.csv`](file:///D:/Dormiy-ML/data/final/cv/dormiy_cv_manifest.csv)
- **Total Record:** **50 baris**
- **Jumlah `product_id` Unik:** **50 ID unik**
- **Pemeriksaan Duplikasi:** `False` (0 duplikasi terdeteksi).
- **Distribusi Status Unduh:**
  - `SUCCESS`: **50 produk (100.0%)**
  - `FAILED`: 0 produk
- **Hasil:** **PASS**

---

### B. Pemeriksaan 2: Validasi Fisik & Integritas File Gambar
- **Direktori Diperiksa:** [`data/final/cv/images/`](file:///D:/Dormiy-ML/data/final/cv/images/)
- **Jumlah File Fisik:** **50 file** (ekstensi `.jpg`)
- **Pencocokan Manifest vs Fisik:** Seluruh 50 `product_id` yang tercatat pada manifest ditemukan 1:1 di direktori fisik.
- **Pengujian Integritas dengan Pillow:**
  - `Image.open().verify()`: **50 / 50 lolos (100%)**
  - File rusak/corrupted: **0 file**
  - Format citra terverifikasi: **100% JPEG**
  - Rentang resolusi: minimum $200 \times 200$ px hingga maksimum $3545 \times 2364$ px.
  - Komposisi transparansi: Seluruh gambar dengan alpha channel telah terpadu ke latar belakang putih solid.
- **Hasil:** **PASS**

---

### C. Pemeriksaan 3: Validasi Relasi Data (CV Manifest vs NLP Catalog)
- **Sumber Data:**
  - Manifest CV: [`data/final/cv/dormiy_cv_manifest.csv`](file:///D:/Dormiy-ML/data/final/cv/dormiy_cv_manifest.csv) (50 produk)
  - Katalog NLP: [`data/final/nlp/dormiy_nlp_catalog.csv`](file:///D:/Dormiy-ML/data/final/nlp/dormiy_nlp_catalog.csv) (337 produk)
  - Dataset Bersih Master: [`data/processed/dormiy_products_clean.csv`](file:///D:/Dormiy-ML/data/processed/dormiy_products_clean.csv) (1.000 produk)
- **Hasil Pencocokan:**
  - **43 dari 50 gambar (86.0%)** berpasangan langsung dengan produk aktif pada katalog kandidat NLP (`dormiy_nlp_catalog.csv`):
    - 11 produk berstatus `Approved_NLP` (misal: `prod_0474`, `prod_0510`, `prod_0394`, `prod_0719`).
    - 30 produk berstatus `Candidate_NLP` (batch gambar tambahan).
    - 2 produk berstatus `Candidate_Review` (perkakas pemeliharaan `prod_0273` dan `prod_0802`).
  - **7 dari 50 gambar (14.0%)** tidak ditemukan di `dormiy_nlp_catalog.csv`:
    - Produk: `prod_0008` (pisau lipat), `prod_0054` (mesin tabber), `prod_0583` (garden arbor), `prod_0659` (rolling papers), `prod_0672` (perlengkapan bayi), `prod_0751` (police scanner), `prod_0892` (konektor PCB).
    - **Analisis Relasi:** Ketujuh produk ini **secara sengaja dikeluarkan dari katalog NLP** (berstatus `Excluded_NLP`) berdasarkan kriteria kurasi asrama (`reports/final_dataset_curation_criteria.md`), tetapi aset gambarnya tetap dipertahankan pada manifest CV sebagai bukti empiris hasil inspeksi visual pilot. Seluruh 7 produk ini tetap memiliki pasangan data lengkap pada master dataset `data/processed/dormiy_products_clean.csv`.
- **Hasil:** **PASS (With Note)**

---

### D. Pemeriksaan 4: Validasi Katalog NLP (CSV vs JSON)
- **File Diperiksa:**
  - CSV: [`data/final/nlp/dormiy_nlp_catalog.csv`](file:///D:/Dormiy-ML/data/final/nlp/dormiy_nlp_catalog.csv)
  - JSON: [`data/final/nlp/dormiy_nlp_catalog.json`](file:///D:/Dormiy-ML/data/final/nlp/dormiy_nlp_catalog.json)
- **Jumlah Baris:** **Tepat 337 record** pada CSV dan JSON.
- **Pemeriksaan Duplikasi:** `False` (0 duplikasi `product_id`).
- **Kelengkapan Kolom Teks:**
  - Missing/NaN `text_for_nlp` pada CSV: **0**
  - Missing/null `text_for_nlp` pada JSON: **0**
- **Rekonsiliasi Atribut per Atribut (Attribute-by-Attribute Match):**
  - Seluruh 12 kolom (`product_id`, `title`, `clean_title`, `text_for_nlp`, `main_category`, `sub_category`, `brand_imputed`, `is_secondhand`, `relevance_label`, `needs_review`, `curation_status`, `curation_reason`) dicocokkan record per record antara CSV dan JSON.
  - Jumlah ketidakcocokan nilai: **0 mismatch (100% identik)**.
  - Missing values pada JSON tersimpan sesuai standar valid `null` (bebas dari `NaN`).
- **Hasil:** **PASS**

---

### E. Pemeriksaan 5: Validasi Struktur & Ketersediaan File Final
Pemeriksaan eksistensi dan ukuran file pada direktori final:

| Path File / Direktori | Tipe | Status Eksistensi | Ukuran Aktual |
| :--- | :---: | :---: | :--- |
| `data/final/nlp/dormiy_nlp_catalog.csv` | File | **Tersedia** | 381.703 bytes (~372 KB) |
| `data/final/nlp/dormiy_nlp_catalog.json` | File | **Tersedia** | 480.077 bytes (~468 KB) |
| `data/final/cv/dormiy_cv_manifest.csv` | File | **Tersedia** | 30.941 bytes (~30 KB) |
| `data/final/cv/images/` | Direktori | **Tersedia** | 50 file JPEG valid |
| `reports/final_dataset_preparation_report.md` | File | **Tersedia** | 6.435 bytes (~6.2 KB) |

- **Hasil:** **PASS**

---

## 3. Daftar Temuan & Catatan Teknis (Notes for Handoff)

1. **Catatan untuk Tim NLP (Farhan):**
   - Katalog utama `data/final/nlp/dormiy_nlp_catalog.csv` (dan `.json`) berisi **337 produk** yang siap digunakan untuk pemodelan semantic search / retrieval.
   - Kolom `text_for_nlp` telah terbebas dari missing values dan telah menggabungkan judul, kategori, brand, serta deskripsi yang dinormalisasi.
   - Perhatikan kolom `curation_status`:
     - `Approved_NLP` (11 produk): Prioritas utama pengujian akurasi pencarian.
     - `Candidate_NLP` (322 produk): Produk bersih yang dapat dijadikan korpus penelusuran.
     - `Candidate_Review` (4 produk): Ditandai untuk evaluasi sensitivitas filter pencarian.

2. **Catatan untuk Tim Computer Vision (Noel):**
   - Koleksi gambar `data/final/cv/images/` berisi **50 citra JPEG valid**.
   - Seluruh gambar telah dikompositkan ke latar belakang putih solid (aman dari artefak hitam transparansi).
   - Dari 50 gambar, **43 gambar** memiliki pasangan langsung di katalog aktif `dormiy_nlp_catalog.csv`, sedangkan **7 gambar** merupakan produk *negative sample / excluded* dari hasil pilot review yang tetap dapat digunakan untuk pengujian klasifikasi *out-of-scope / rejection*.
   - Lembar kontak visual untuk inspeksi cepat tersedia di:
     - `reports/figures/pilot_image_contact_sheet.jpg` (20 gambar pilot).
     - `reports/figures/additional_images_contact_sheet.jpg` (30 gambar tambahan).

---

## 4. Kesimpulan & Rekomendasi Status Akhir

### Kesimpulan:
Berdasarkan hasil verifikasi aktual terhadap 5 komponen pengujian, seluruh file output berada dalam kondisi lengkap, valid, bebas dari kerusakan teknis (*zero corrupt*), dan konsisten antarformat (*zero discrepancy*). Tidak ditemukan adanya pelanggaran integritas data pada data sumber maupun keluaran final.

### Rekomendasi Status Akhir Task:
> ### **STATUS: DONE (SIAP DISERAHKAN)**
> Seluruh deliverable untuk task **Dataset Preparation, EDA & Cleaning** telah selesai dan memenuhi acceptance criteria. Dataset final siap diserahkan kepada **Farhan (Tim NLP)** dan **Noel (Tim Computer Vision)** untuk melangkah ke tahap feature extraction dan pemodelan machine learning.

