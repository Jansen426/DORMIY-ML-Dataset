# Laporan Final Dataset Preparation, EDA & Cleaning - Proyek DORMIY

**Tanggal:** 10 November 2026  
**Status Fase:** Selesai (Finalized)  
**Dokumen Terkait:**
- Standar Kurasi: [`reports/final_dataset_curation_criteria.md`](file:///D:/Dormiy-ML/reports/final_dataset_curation_criteria.md)
- Audit Kurasi: [`reports/final_curation_audit.md`](file:///D:/Dormiy-ML/reports/final_curation_audit.md)
- Ekspor Katalog NLP: [`reports/nlp_dataset_export_summary.md`](file:///D:/Dormiy-ML/reports/nlp_dataset_export_summary.md)
- Review Visual Pilot: [`reports/pilot_image_visual_review.md`](file:///D:/Dormiy-ML/reports/pilot_image_visual_review.md)

---

## 1. Ringkasan Eksekutif & Struktur Final

Fase **Dataset Preparation, Exploratory Data Analysis (EDA), dan Data Cleaning** untuk proyek DORMIY telah diselesaikan secara praktis dengan membagi dataset ke dalam dua jalur terpisah (*Dual-Track Architecture*): Jalur NLP (Pencarian Teks Semantik) dan Jalur Computer Vision (Retrieval Visual Multimodal).

### Struktur Direktori Final:
- **Jalur NLP:**
  - `data/final/nlp/dormiy_nlp_catalog.csv` (337 produk, 12 kolom metadata bersih).
  - `data/final/nlp/dormiy_nlp_catalog.json` (337 record, standar validasi JSON `null`).
- **Jalur Computer Vision:**
  - `data/final/cv/dormiy_cv_manifest.csv` (50 record gambar terverifikasi dengan path lokal final).
  - `data/final/cv/images/` (50 file citra JPEG terkompositkan background putih, 100% lolos validasi Pillow).
- **Contact Sheet Verifikasi Visual:**
  - `reports/figures/pilot_image_contact_sheet.jpg` (20 gambar sampel pilot pertama).
  - `reports/figures/additional_images_contact_sheet.jpg` (30 gambar sampel tambahan).

---

## 2. Metrik Kuantitatif Dataset

### A. Dataset NLP (Katalog Pencarian Teks)
- **Kandidat Awal (`relevance_label == 'Relevant'`):** 344 produk.
- **Excluded_NLP:** 7 produk (dikeluarkan dari katalog kandidat berdasarkan hasil review manual pilot).
- **Total Produk Masuk Katalog NLP:** **337 produk** (100% memiliki `text_for_nlp` valid, 0 duplikasi).
- **Distribusi Status Kurasi NLP:**
  - `Approved_NLP`: 11 produk (3.2%) — Terkonfirmasi relevan untuk fasilitas asrama melalui evaluasi manual.
  - `Candidate_NLP`: 322 produk (95.5%) — Kandidat bersih yang lolos screening kata kunci negatif, menunggu kurasi manual bertahap.
  - `Candidate_Review`: 4 produk (1.2%) — Terdeteksi indikasi kata kunci negatif / perkakas teknis, ditandai untuk peninjauan khusus (tidak otomatis dibuang).

### B. Dataset Computer Vision (Aset Gambar)
- **Target Unduh Gambar Pilot (Batch 1):** 20 produk.
  - Berhasil diunduh & divalidasi: 20 gambar (100%).
  - Gagal: 0 gambar.
- **Target Unduh Gambar Tambahan (Batch 2):** 30 produk (6 produk per kategori dari 5 kategori inti).
  - Berhasil diunduh & divalidasi: 30 gambar (100%).
  - Gagal: 0 gambar.
- **Total Gambar Berhasil:** **50 gambar JPEG** (20 pilot + 30 tambahan).
- **Total Gambar Gagal:** **0 gambar**.
- **Validasi Pillow:** Seluruh 50 file gambar diuji menggunakan `Image.open().verify()` dengan tingkat keberhasilan 100% (0 corrupt).
- **Penanganan Transparansi:** Seluruh gambar dengan alpha channel (RGBA/LA/PA) dikompositkan ke latar belakang putih solid sebelum disimpan dalam format JPEG untuk mencegah artefak hitam.

---

## 3. Hasil Validasi Integritas Data

1. **Perlindungan Data Mentah & Bersih (*Zero Data Loss*):**
   - File mentah asli `data/raw/shopify_sample_1000.csv` dan file bersih `data/processed/dormiy_products_clean.csv` (1.000 baris, 23 kolom) tetap utuh 100% tanpa ada baris atau kolom yang terhapus/berubah.
2. **Konsistensi Format CSV dan JSON:**
   - Seluruh 337 record dan 12 atribut pada `data/final/nlp/dormiy_nlp_catalog.csv` dan `.json` terbukti identik atribut per atribut (rekonsiliasi 100%).
3. **Ketiadaan Duplikasi:**
   - Tidak ada duplikasi `product_id` pada katalog NLP maupun manifest CV.

---

## 4. Keterbatasan Dataset (Dataset Limitations)

1. **Dataset Shopify sebagai Proxy Katalog Publik:**
   - Dataset yang digunakan berasal dari *Shopify Product Catalogue* yang bersifat publik dan komersial/e-commerce. Dataset ini **bukan inventaris aktual gudang fisik asrama RTB**.
   - Terminologi produk merefleksikan bahasa e-commerce ritel multinasional sehingga pencarian inventaris memerlukan pemetaan sinonim (*domain synonym mapping*).
2. **Keterbatasan Kurasi Manual:**
   - **Tidak semua produk dapat diklaim relevan secara manual.** Dari 337 produk katalog NLP, baru 11 produk yang berstatus `Approved_NLP` dan 7 produk berstatus `Excluded_NLP`. Sisanya (322 produk) masih berstatus `Candidate_NLP` dan 4 produk `Candidate_Review`.
   - Pada dataset CV, 20 gambar pertama telah melalui inspeksi visual terperinci (`reports/pilot_image_visual_review.md`), sedangkan 30 gambar tambahan telah diverifikasi integritas teknisnya via Pillow dan contact sheet, namun belum seluruhnya diinspeksi fungsi asramanya satu per satu.
3. **Representasi Visual:**
   - Sebagian kecil gambar memiliki format sketsa/diagram teknis (`prod_0741`) atau rasio aspek sempit/memanjang (`prod_0569`) yang memerlukan teknik letterboxing/padding saat diproses oleh Vision Transformer.

---

## 5. Status Acceptance Criteria

| Kriteria Penerimaan (Acceptance Criteria) | Status | Bukti & Lokasi Verifikasi |
| :--- | :---: | :--- |
| **Exploratory Data Analysis (EDA)** | **TERPENUHI (DONE)** | EDA komprehensif, visualisasi top-kategori dan distribusi teks di `reports/figures/01_*.png`, `02_*.png`, `03_*.png`. |
| **Data Cleaning & Preprocessing Teks** | **TERPENUHI (DONE)** | 1.000 data utuh, imputasi brand generic, penanganan deskripsi kosong, dan pemisahan subkategori di `data/processed/dormiy_products_clean.csv`. |
| **Pilot Image Pipeline & Validasi Transparansi** | **TERPENUHI (DONE)** | Streaming Hugging Face, komposit background putih, dan contact sheet di `reports/figures/pilot_image_contact_sheet.jpg`. |
| **Pemisahan Jalur Dataset (NLP & CV)** | **TERPENUHI (DONE)** | Struktur final terpisah di `data/final/nlp/` (337 produk) dan `data/final/cv/` (50 gambar + manifest). |
| **Verifikasi Integritas & Bebas Duplikasi** | **TERPENUHI (DONE)** | Seluruh 50 gambar lolos uji Pillow (0 corrupt), 0 duplikasi ID, 0 text_for_nlp kosong, dataset cleaned utuh. |
| **Dokumentasi & Kriteria Kurasi Terstruktur** | **TERPENUHI (DONE)** | Dokumen standar kurasi, laporan audit, laporan inspeksi visual, dan ringkasan ekspor tersimpan lengkap di `reports/`. |

