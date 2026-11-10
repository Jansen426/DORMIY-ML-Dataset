# Laporan Ekspor Dataset NLP DORMIY

**Tanggal:** 10 November 2026  
**File Output CSV:** [`data/final/dormiy_nlp_catalog.csv`](file:///D:/Dormiy-ML/data/final/dormiy_nlp_catalog.csv)  
**File Output JSON:** [`data/final/dormiy_nlp_catalog.json`](file:///D:/Dormiy-ML/data/final/dormiy_nlp_catalog.json)  
**Dataset Sumber:** [`data/processed/dormiy_products_clean.csv`](file:///D:/Dormiy-ML/data/processed/dormiy_products_clean.csv) (1.000 produk)  
**Dokumen Standar:** [`reports/final_dataset_curation_criteria.md`](file:///D:/Dormiy-ML/reports/final_dataset_curation_criteria.md) & [`reports/final_curation_audit.md`](file:///D:/Dormiy-ML/reports/final_curation_audit.md)

---

## 1. Ringkasan Eksekutif Ekspor

Dataset katalog NLP ini diekspor khusus untuk mendukung kebutuhan **Natural Language Processing (Pencarian Semantik, Keyword Search BM25, dan Text Embedding)** pada sistem inventaris asrama DORMIY. Sesuai prinsip *Dual-Track Architecture*, dataset NLP berfokus pada kualitas metadata tekstual (`clean_title`, `text_for_nlp`, `brand_imputed`, `main_category`, `sub_category`).

Seluruh angka dan persentase dihitung secara dinamis dari hasil aktual kurasi dan screening:

| Status Kurasi NLP | Jumlah Produk | Persentase dari 344 | Keterangan & Tindak Lanjut |
| :--- | :---: | :---: | :--- |
| **Approved_NLP** | **11** | **3.2%** | **Terkonfirmasi Relevan:** Diverifikasi manual memiliki teks yang sangat relevan untuk operasional/fasilitas asrama. |
| **Candidate_NLP** | **322** | **93.6%** | **Kandidat Bersih:** Lolos screening kata kunci negatif, menunggu kurasi manual bertahap. |
| **Candidate_Review** | **4** | **1.2%** | **Kandidat Butuh Review:** Terdeteksi screening kata kunci negatif / perkakas bengkel pemeliharaan (tidak otomatis dikeluarkan). |
| **Excluded_NLP (Dikeluarkan)** | **7** | **2.0%** | **Eksklusi Terkonfirmasi:** Dipastikan tidak relevan untuk asrama berdasarkan hasil inspeksi pilot. |
| **TOTAL KATALOG KANDIDAT NLP** | **337** | **98.0%** | Terdiri dari `Approved_NLP`, `Candidate_NLP`, dan `Candidate_Review`. |

> [!NOTE]
> Nilai `relevance_label` pada data sumber (`dormiy_products_clean.csv`) tetap dipertahankan 100% tanpa perubahan (*zero data loss*). Seluruh keputusan kurasi dicatat secara eksplisit pada kolom `curation_status` dan `curation_reason`.

---

## 2. Rincian Produk Approved_NLP (11 Produk)

Produk-produk ini telah diverifikasi secara manual memiliki relevansi tekstual langsung dengan fasilitas dan operasional asrama:

| product_id | main_category | title | Alasan Persetujuan NLP |
| :--- | :--- | :--- | :--- |
| `prod_0064` | Office Supplies | PATIKIL 6 Pcs Desk Call Bell 2.5" Dia with Metal Anti-Rust C | Terkonfirmasi relevan untuk inventaris asrama (Pilot Review) |
| `prod_0235` | Electronics | Tischaufsteller fürs Mikrofon Newskill NS-AC-KALIOPE LED Sch | Terkonfirmasi relevan untuk inventaris asrama (Pilot Review) |
| `prod_0238` | Hardware | TRUSCO 防振パット 耐熱耐油性 シートタイプ 300X300X10 OH10CR トラスコ | Terkonfirmasi relevan untuk inventaris asrama (Pilot Review) |
| `prod_0394` | Electronics | Nintendo Switch Power Cable | Terkonfirmasi relevan untuk inventaris asrama (Pilot Review) |
| `prod_0474` | Furniture | 4 Tier Bookshelf, Bookcase, Etagere, Corner, For Office, Con | Terkonfirmasi relevan untuk inventaris asrama (Pilot Review) |
| `prod_0510` | Furniture | Ralis White & Oak Kitchen Cupboard - 5 Door | Terkonfirmasi relevan untuk inventaris asrama (Pilot Review) |
| `prod_0569` | Home & Garden | WOOD HANDLE LAQ WOOD THRD 15/16 IN X 60 | Terkonfirmasi relevan secara tekstual untuk inventaris asrama (Manual review CV karena visual: Gambar menampilkan gagang kayu berthearding/ulir untuk perkakas pembersih (sapu/pel). Gambar tajam namun terpotong sangat panjang/sempit (aspek rasio ekstrem 432x65 px). Cocok untuk inventaris kebersihan asrama.) |
| `prod_0719` | Office Supplies | STAPLER-HEAVY DUTY BOSTITCH 65 PREMIUM | Terkonfirmasi relevan untuk inventaris asrama (Pilot Review) |
| `prod_0741` | Furniture | Shaker Cinder 24" W x 36" H Wall Diagonal Glass Door Corner  | Terkonfirmasi relevan secara tekstual untuk inventaris asrama (Manual review CV karena visual: Gambar merupakan sketsa/garis gambar teknik (blueprint diagram dimensi beranotasi ukuran) lemari kabinet sudut dinding. Produknya relevan (lemari kabinet asrama), namun gambarnya berupa diagram teknis bukan foto produk/furnitur realistik.) |
| `prod_0786` | Office Supplies | Ultimate Office Mesh Wall File Organizer, 12 Tier Vertical M | Terkonfirmasi relevan untuk inventaris asrama (Pilot Review) |
| `prod_0792` | Home & Garden | Big Green Egg SpeediClean™ Palmyra Bristle Long-Handle Grid  | Terkonfirmasi relevan untuk inventaris asrama (Pilot Review) |

---

## 3. Rincian Produk Candidate_Review (4 Produk)

Produk-produk ini **tidak langsung dikeluarkan secara sepihak**, melainkan ditandai untuk peninjauan manual khusus karena terdeteksi pola kata kunci negatif atau merupakan perkakas pemeliharaan teknis:

| product_id | main_category | title | Alasan Peninjauan (curation_reason) |
| :--- | :--- | :--- | :--- |
| `prod_0106` | Furniture | Valkoinen lasten sängynrunko laatikoilla Sipe 70x140cm (mänt | Terdeteksi screening kata kunci negatif: Terdeteksi indikasi perabot/perlengkapan bayi & anak kecil di luar profil asrama umum |
| `prod_0273` | Hardware | Sioux Tools - 1/4" Bit Holder, 700 RPM, Pistol Grip Handle A | Perkakas pemeliharaan teknis fasilitas asrama; memerlukan peninjauan kebijakan operasional asrama |
| `prod_0593` | Electronics | H400G Car 3.5 inch GPS Mode HUD Head-up Display Support Spee | Terdeteksi screening kata kunci negatif: Terdeteksi indikasi produk konsumsi tembakau/rokok/vaping; Terdeteksi indikasi aksesoris/suku cadang kendaraan pribadi di luar fasilitas gedung |
| `prod_0802` | Hardware | Brush Research Mfg. - 1-1/4" Diam Helical Steel Tube Brush - | Perkakas pemeliharaan teknis fasilitas asrama; memerlukan peninjauan kebijakan operasional asrama |

---

## 4. Rincian Produk Excluded_NLP (7 Produk yang Dikeluarkan)

Produk-produk ini berasal dari kandidat awal `Relevant`, namun dipastikan keluar dari katalog NLP berdasarkan keputusan review pilot yang terkonfirmasi:

| product_id | main_category | title | Alasan Eksklusi |
| :--- | :--- | :--- | :--- |
| `prod_0008` | Hardware | SOG SEAL XR 3.9" Folding Pocket Knife (Blackout) | Eksklusi terkonfirmasi (Pilot Review): Gambar jelas menampilkan pisau lipat taktis hitam (folding pocket knife) pada latar belakang putih. Pisau saku/taktis bukan merupakan inventaris resmi asrama dan berpotensi melanggar regulasi keamanan asrama. |
| `prod_0054` | Office Supplies | FORMAX FD 262 Single-Head Tabber | Eksklusi terkonfirmasi (Pilot Review): Gambar menampilkan mesin tabber industri berat untuk pemrosesan surat/dokumen massal. Mesin kantor industri berat tidak relevan untuk inventaris standar asrama. |
| `prod_0583` | Home & Garden | Outvita 7FT Garden Arch Arbor with Seating, Heavy Duty Metal | Eksklusi terkonfirmasi (Pilot Review): Gambar sangat jelas menampilkan gerbang lengkung taman (garden arbor) berbahan besi dengan bangku duduk berhias bunga untuk pesta/taman luar ruang. Tidak relevan untuk inventaris kamar/fasilitas standar asrama mahasiswa. |
| `prod_0659` | Home & Garden | Elements Ultimate Thin Single Wide Rolling Papers (Display o | Eksklusi terkonfirmasi (Pilot Review): Gambar jelas menampilkan kotak display kemasan kertas linting rokok (rolling papers). Merupakan produk konsumsi/aksesori rokok, tidak relevan dan bertentangan dengan kebutuhan inventaris asrama. |
| `prod_0672` | Furniture | Safety 1st Pathways Home 2-piece Set, Highchair and Bassinet | Eksklusi terkonfirmasi (Pilot Review): Gambar jelas menampilkan kursi makan bayi tinggi (highchair) dan ranjang bayi pada latar belakang putih. Merupakan perabot bayi/anak kecil, tidak relevan untuk asrama mahasiswa/pekerja. |
| `prod_0751` | Electronics | BCD436HP Uniden Police Scanner (SC) | Eksklusi terkonfirmasi (Pilot Review): Gambar adalah diagram/infografis produk pemindai radio polisi genggam (police scanner) beranotasi lengkap dengan garis penunjuk dan label teks fungsi tombol. Bersifat terlalu spesifik/radio hobi dan tidak relevan untuk asrama. |
| `prod_0892` | Electronics | Phoenix Contact 1702018 | Eksklusi terkonfirmasi (Pilot Review): Gambar menampilkan blok terminal konektor PCB elektronik industri (Phoenix Contact). Komponen elektronik murni, tidak relevan untuk inventaris asrama. |

---

## 5. Distribusi Kategori pada Katalog Kandidat NLP (337 Produk)

| Kategori Utama | Approved_NLP | Candidate_NLP | Candidate_Review | Total Katalog NLP | Proporsi (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Electronics** | 2 | 47 | 1 | **50** | 14.8% |
| **Furniture** | 3 | 26 | 1 | **30** | 8.9% |
| **Hardware** | 1 | 84 | 2 | **87** | 25.8% |
| **Home & Garden** | 2 | 149 | 0 | **151** | 44.8% |
| **Office Supplies** | 3 | 16 | 0 | **19** | 5.6% |
| **TOTAL** | **11** | **322** | **4** | **337** | **100.0%** |

---

## 6. Hasil Uji Validasi Integritas Data

1. **Jumlah Kandidat Awal:** Tepat 344 produk terverifikasi dari `dormiy_products_clean.csv`.
2. **Keluaran Produk Excluded:** Seluruh 7 produk `Excluded_NLP` dipastikan 100% tidak ada di dalam `dormiy_nlp_catalog.csv` maupun `.json`.
3. **Keunikan ID:** Nol duplikasi pada kolom `product_id`.
4. **Kelengkapan Teks:** Nol nilai kosong (`NaN` atau string kosong) pada kolom `text_for_nlp`.
5. **Kesesuaian Kolom:** Seluruh 12 kolom wajib tersedia (`product_id, title, clean_title, text_for_nlp, main_category, sub_category, brand_imputed, is_secondhand, relevance_label, needs_review, curation_status, curation_reason`).
6. **Konsistensi Format:** File CSV dan JSON telah divalidasi atribut per atribut untuk seluruh 337 entri dan terbukti 100% identik.
7. **Perlindungan Data Mentah:** File sumber `dormiy_products_clean.csv` diverifikasi utuh sebelum dan sesudah eksekusi melalui verifikasi dimensi dan checksum SHA-256.
