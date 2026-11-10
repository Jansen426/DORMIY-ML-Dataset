# Data Cleaning & Modular Preprocessing Report - DORMIY

**Dokumen Laporan Pembersihan Data, Pemisahan Kolom, dan Pelabelan Relevansi**
- **Data Raw Asli:** `data/raw/shopify_sample_1000.csv` (1000 baris, 9 kolom)
- **Data Processed:** `data/processed/dormiy_products_clean.csv` (1000 baris, 23 kolom)
- **Data Processed JSON:** `data/processed/dormiy_products_clean.json` (1000 baris)
- **Ketentuan Utama:** Seluruh 1.000 baris data mentah dipertahankan (Zero Data Loss). Tidak ada baris yang difilter atau dibuang.

## 1. Pemetaan Struktur Kolom Dataset Bersih
| No | Nama Kolom | Jenis | Keterangan & Aturan |
| :---: | :--- | :---: | :--- |
| 1 | `product_id` | Asli (Raw) | Dipertahankan 100% nilai asli |
| 2 | `title` | Asli (Raw) | Dipertahankan 100% nilai asli |
| 3 | `description` | Asli (Raw) | Dipertahankan 100% nilai asli |
| 4 | `category` | Asli (Raw) | Dipertahankan 100% nilai asli |
| 5 | `brand` | Asli (Raw) | Dipertahankan 100% nilai asli |
| 6 | `is_secondhand` | Asli (Raw) | Dipertahankan 100% nilai asli |
| 7 | `potential_categories` | Asli (Raw) | Dipertahankan 100% nilai asli |
| 8 | `has_image` | Asli (Raw) | Dipertahankan 100% nilai asli |
| 9 | `image_url` | Asli (Raw) | Dipertahankan 100% nilai asli |
| 10 | `clean_title` | Preprocessing | Kolom transformasi analitik baru |
| 11 | `clean_description` | Preprocessing | Kolom transformasi analitik baru |
| 12 | `text_for_nlp` | Preprocessing | Kolom transformasi analitik baru |
| 13 | `desc_length` | Preprocessing | Kolom transformasi analitik baru |
| 14 | `description_source` | Preprocessing | Kolom transformasi analitik baru |
| 15 | `brand_imputed` | Preprocessing | Kolom transformasi analitik baru |
| 16 | `is_brand_imputed` | Preprocessing | Kolom transformasi analitik baru |
| 17 | `main_category` | Preprocessing | Kolom transformasi analitik baru |
| 18 | `sub_category` | Preprocessing | Kolom transformasi analitik baru |
| 19 | `image_url_format_valid` | Preprocessing | Kolom transformasi analitik baru |
| 20 | `relevance_label` | Preprocessing | Kolom transformasi analitik baru |
| 21 | `relevance_reason` | Preprocessing | Kolom transformasi analitik baru |
| 22 | `needs_review` | Preprocessing | Kolom transformasi analitik baru |
| 23 | `is_dorm_relevant` | Preprocessing | Kolom transformasi analitik baru |

## 2. Ringkasan Kualitas dan Pelabelan
- **Missing Description Asli:** 63 produk (6.3%)
  * Ditangani via `text_for_nlp` dengan fallback judul (`description_source = 'title_fallback'`).
- **Missing Brand Asli:** 30 produk (3.0%)
  * Diimputasi ke kolom `brand_imputed = 'Generic'`, sementara kolom `brand` asli tetap bernilai `NaN`.
- **Validasi Format URL Gambar (`image_url_format_valid`):** 1000 / 1000 valid berawalan HTTP/HTTPS.

### Distribusi Relevansi Inventaris:
- **Maybe Relevant:** 428 produk (42.8%)
- **Relevant:** 344 produk (34.4%)
- **Irrelevant:** 228 produk (22.8%)
- **Produk Perlu Review Kurasi (`needs_review = True`):** 83 produk (8.3%)