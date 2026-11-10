# Laporan Audit Kurasi Kandidat Produk DORMIY

**Tanggal Audit:** 10 November 2026  
**Dokumen Acuan:**
1. [`data/processed/dormiy_products_clean.csv`](file:///D:/Dormiy-ML/data/processed/dormiy_products_clean.csv) (1.000 produk hasil data cleaning)
2. [`reports/final_dataset_curation_criteria.md`](file:///D:/Dormiy-ML/reports/final_dataset_curation_criteria.md) (Kriteria kurasi produk & gambar)
3. [`reports/pilot_image_visual_review.md`](file:///D:/Dormiy-ML/reports/pilot_image_visual_review.md) (Hasil inspeksi visual 20 sampel pilot)

---

## 1. Ringkasan Eksekutif Audit

Audit ini dilakukan untuk memverifikasi kesiapan kurasi kandidat inventaris asrama DORMIY pada seluruh produk yang memiliki klasifikasi awal `relevance_label == "Relevant"`. Berdasarkan standar kurasi *Dual-Track Architecture*, label awal `Relevant` dari proses cleaning otomatis **tidak menjamin produk otomatis masuk ke dataset final**, melainkan harus diverifikasi melalui inspeksi manual (teks kontekstual dan aset visual).

| Metrik Audit | Jumlah Produk | Persentase | Status & Catatan |
| :--- | :---: | :---: | :--- |
| **Total Kandidat Awal (`relevance_label == "Relevant"`)** | **344** | **100.0%** | Hasil filter heuristik kategori utama pada `05_data_cleaning.py`. |
| **Sudah Dikurasi Manual & Memiliki Visual Review** | **20** | **5.8%** | Sampel pilot yang telah diunduh gambarnya dan diperiksa pada contact sheet. |
| **Belum Dikurasi Manual (Pending Verification)** | **324** | **94.2%** | Memiliki metadata teks bersih, namun belum diperiksa secara manual maupun visual. |

> [!IMPORTANT]
> Seluruh **324 produk yang belum diperiksa TIDAK BOLEH diasumsikan sebagai `Keep`**. Berdasarkan temuan pilot, 35% produk dari kategori awal `Relevant` terbukti `Irrelevant` (seperti rokok `prod_0659` dan pisau taktis `prod_0008`) dan 20% memerlukan `Manual Review` (seperti blueprint teknis `prod_0741` dan rasio aspek ekstrem `prod_0569`).

---

## 2. Status Kurasi 20 Sampel Pilot (Telah Diperiksa Manual)

Seluruh 20 produk pilot yang telah diperiksa visualnya berasal dari kelompok 344 kandidat `Relevant` (terpilih secara acak terstratifikasi, masing-masing 4 produk dari 5 kategori utama).

### Ringkasan Keputusan Kurasi 20 Sampel Pilot:
- **Keep:** 9 produk (45.0%) — Produk relevan dengan foto fisik yang tajam dan layak untuk baseline CV.
- **Manual Review:** 4 produk (20.0%) — Produk fungsional relevan namun memiliki anomali gambar (blueprint/rasio ekstrem) atau perkakas bengkel pemeliharaan.
- **Exclude:** 7 produk (35.0%) — Produk yang setelah diverifikasi tidak sesuai dengan kebutuhan/regulasi fasilitas asrama.

### Rincian Keputusan per Produk:

#### A. Keputusan: KEEP (9 Produk)
*Produk terkonfirmasi relevan untuk asrama dan memiliki foto produk riil berkualitas baik untuk baseline Computer Vision:*
1. `prod_0792` — *Big Green Egg SpeediClean™ Palmyra Bristle Long-Handle Grid Scrubber* (Home & Garden: sikat pembersih grill/dapur).
2. `prod_0238` — *TRUSCO 防振パット 耐熱耐油性 シートタイプ 300X300X10 OH10CR トラスコ* (Hardware: bantalan peredam getaran mesin cuci/kulkas).
3. `prod_0394` — *Nintendo Switch Power Cable* (Electronics: kabel daya/charger).
4. `prod_0235` — *Tischaufsteller fürs Mikrofon Newskill NS-AC-KALIOPE LED Schwarz* (Electronics: mikrofon meja & stand podium).
5. `prod_0474` — *4 Tier Bookshelf, Bookcase, Etagere, Corner, For Office* (Furniture: rak buku sudut kamar asrama - lifestyle photo).
6. `prod_0510` — *Ralis White & Oak Kitchen Cupboard - 5 Door* (Furniture: lemari dapur bersama - lifestyle photo).
7. `prod_0786` — *Ultimate Office Mesh Wall File Organizer, 12 Tier Vertical Mount* (Office Supplies: rak gantung dinding organizer dokumen).
8. `prod_0719` — *STAPLER-HEAVY DUTY BOSTITCH 65 PREMIUM* (Office Supplies: stapler meja tugas berat).
9. `prod_0064` — *PATIKIL 6 Pcs Desk Call Bell 2.5" Dia Metal Construction* (Office Supplies: bel meja resepsionis/front desk asrama).

#### B. Keputusan: MANUAL REVIEW (4 Produk)
*Produk relevan secara fungsional untuk inventaris/pemeliharaan asrama, namun memerlukan keputusan khusus tim kurator:*
1. `prod_0569` — *WOOD HANDLE LAQ WOOD THRD 15/16 IN X 60* (Home & Garden: gagang kayu pel/sapu. Kualitas fair, aspek rasio ekstrem 432x65 px, butuh penanganan padding).
2. `prod_0802` — *Brush Research Mfg. Helical Steel Tube Brush* (Hardware: sikat kawat baja pembersih pipa industri. Relevan untuk divisi maintenance/plumbing, bukan inventaris kamar).
3. `prod_0273` — *Sioux Tools Pistol Grip Handle Air Screwdriver* (Hardware: obeng bertenaga angin. Relevan untuk teknisi pemeliharaan gedung asrama).
4. `prod_0741` — *Shaker Cinder Wall Diagonal Glass Door Corner Cabinet* (Furniture: lemari kabinet dapur sangat relevan, namun gambarnya berupa diagram garis teknis/blueprint berdimensi inci, bukan foto produk).

#### C. Keputusan: EXCLUDE (7 Produk)
*Produk yang dibatalkan status relevansinya karena terbukti tidak sesuai untuk asrama atau berpotensi melanggar regulasi:*
1. `prod_0583` — *Outvita 7FT Garden Arch Arbor with Seating* (Home & Garden: gerbang lengkung taman berhias bunga untuk pesta/pernikahan luar ruang).
2. `prod_0659` — *Elements Ultimate Thin Single Wide Rolling Papers* (Home & Garden: kertas linting rokok/tembakau, barang konsumsi personal terlarang di asrama).
3. `prod_0008` — *SOG SEAL XR 3.9" Folding Pocket Knife* (Hardware: pisau lipat taktis hitam, melanggar regulasi keamanan asrama).
4. `prod_0751` — *BCD436HP Uniden Police Scanner (SC)* (Electronics: pemindai radio frekuensi polisi & gambar infografis diagram tombol).
5. `prod_0892` — *Phoenix Contact 1702018* (Electronics: blok terminal konektor PCB elektronik murni).
6. `prod_0672` — *Safety 1st Pathways Home 2-piece Set, Highchair and Bassinet* (Furniture: kursi makan bayi tinggi & ranjang bayi, di luar profil penghuni asrama).
7. `prod_0054` — *FORMAX FD 262 Single-Head Tabber* (Office Supplies: mesin industri berat pemroses surat massal).

---

## 3. Profil 324 Produk yang Belum Dikurasi Manual

Sebanyak **324 produk kandidat awal belum diperiksa secara manual**. Rincian komposisi kategorinya adalah sebagai berikut:

| Kategori Utama | Total Awal | Sudah Dikurasi (Pilot) | Belum Dikurasi | Proporsi Belum Dikurasi |
| :--- | :---: | :---: | :---: | :---: |
| **Home & Garden** | 153 | 4 | **149** | 46.0% |
| **Hardware** | 88 | 4 | **84** | 25.9% |
| **Electronics** | 52 | 4 | **48** | 14.8% |
| **Furniture** | 31 | 4 | **27** | 8.3% |
| **Office Supplies** | 20 | 4 | **16** | 4.9% |
| **TOTAL** | **344** | **20** | **324** | **100.0%** |

### Contoh Sampel Produk yang Belum Diperiksa (Menunggu Verifikasi):
- **Home & Garden:**
  - `prod_0004`: *Column capital KK13* (ornamen arsitektur mahkota kolom).
  - `prod_0019`: *2018 Autumn Girl* (dekorasi pajangan musiman / figur).
- **Hardware:**
  - `prod_0013`: *PHILIP PN SMS Z 10X7/8* (baut/sekrup kecil).
  - `prod_0021`: *Brizo Touch-Clean Square Body Spray* (nozel semprotan shower mandi).
- **Electronics:**
  - `prod_0007`: *Vishay LED Displays TDSG1160* (komponen modul display LED industri).
  - `prod_0009`: *Florida Gators PS5 VarsityWrapz* (stiker skin konsol game).
- **Furniture:**
  - `prod_0034`: *Anrichte DKD Home Decor Mango-Holz* (meja bufet/lemari samping kayu).
  - `prod_0069`: *HOMCOM End of Bed Bench, Window Seat* (bangku panjang ujung tempat tidur).
- **Office Supplies:**
  - `prod_0110`: *Quality Park Poly Mailer Envelopes* (amplop kemasan pos pengiriman).
  - `prod_0173`: *EXTRACTOR DE AIRE* (exhaust fan/ventilasi udara kantor).

---

## 4. Rekomendasi Cara Melanjutkan Kurasi Secara Bertahap

Untuk menyelesaikan kurasi 324 produk yang tersisa tanpa membebani proses manual sekaligus menjaga kualitas dataset final, direkomendasikan pendekatan kurasi bertingkat (*Tiered Curation Approach*):

```
                      [ 324 Produk Belum Dikurasi ]
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
  [ JALUR NLP (Teks Saja) ]                        [ JALUR COMPUTER VISION ]
  Tahap 1: Text Heuristic Scrubbing                Tahap 1: Batch Download Gambar
  (Singkirkan rokok, senjata, ornamen bayi)        (50-100 gambar bertahap via streaming)
         │                                                   │
         ▼                                                   ▼
  Tahap 2: Validasi Cepat Metadata                 Tahap 2: Contact Sheet Inspection
  (Cek kesesuaian fasilitas asrama)                (Verifikasi Visual Match & Kualitas)
         │                                                   │
         ▼                                                   ▼
  [ Dataset Final NLP (Katalog Teks) ]             [ Dataset Final CV (Multimodal) ]
```

### Rekomendasi Langkah Kerja Konkret:

1. **Jalur NLP (Ekspor Cepat Katalog Pencarian Teks):**
   - **Langkah 1 (Rule-based Exclusion):** Terapkan filter kata kunci negatif otomatis terhadap 324 produk untuk membuang anomali yang mirip dengan temuan pilot (misal: *rolling papers, cigarette, knife, tactical, baby, infant, pcb connector, industrial mailer*).
   - **Langkah 2 (Batch Review Metadata):** Lakukan review berbasis teks cepat per kategori (dimulai dari kategori terkecil: `Office Supplies` 16 item dan `Furniture` 27 item).
   - **Langkah 3:** Produk yang lolos validasi teks langsung dipromosikan ke katalog final NLP tanpa harus menunggu pengunduhan gambar.

2. **Jalur Computer Vision (Kurasi Gambar Multimodal):**
   - **Langkah 1 (Selective Batch Streaming):** Jangan mengunduh seluruh 324 gambar sekaligus. Ambil batch 50 gambar dari produk yang sudah terbukti lolos validasi teks NLP.
   - **Langkah 2 (Generate Contact Sheet per Batch):** Buat contact sheet untuk setiap batch (seperti `pilot_image_contact_sheet.jpg`) agar kurator manusia dapat memeriksa 50 gambar dalam hitungan menit.
   - **Langkah 3 (Terapkan 4 Kriteria Keep):** Terapkan kriteria resmi: relevansi produk terkonfirmasi, `visual_match == "Yes"`, kualitas memadai, dan tipe berupa foto fisik produk (bukan blueprint/diagram).
   - **Langkah 4 (Manifest Logging):** Catat setiap batch hasil kurasi secara atomik ke manifest.

3. **Status Penyimpanan:**
   - Pertahankan seluruh hasil pembersihan pada `dormiy_products_clean.csv`.
   - Buat kolom kurasi final atau file katalog terpisah (`data/final/dormiy_nlp_catalog.csv` dan `data/final/dormiy_cv_manifest.csv`) untuk menyimpan status kurasi tanpa mengubah data mentah asli.

