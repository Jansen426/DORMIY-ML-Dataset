# Laporan Visual Review Pilot Image Dataset DORMIY

**Tanggal:** 10 November 2026  
**File Gambar Sumber:** [`reports/figures/pilot_image_contact_sheet.jpg`](file:///D:/Dormiy-ML/reports/figures/pilot_image_contact_sheet.jpg)  
**Manifest Sumber:** [`data/processed/image_download_manifest.csv`](file:///D:/Dormiy-ML/data/processed/image_download_manifest.csv)  
**Total Sampel:** 20 produk pilot (4 produk per kategori dari 5 kategori utama relevan)

---

## 1. Hasil Visual Inspection (Tabel Evaluasi Per Produk)

| product_id | title | image_type | visual_match | image_quality | dorm_inventory_relevance | reason | recommended_action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `prod_0569` | WOOD HANDLE LAQ WOOD THRD 15/16 IN X 60 | Product Photo (Isolated) | Yes | Fair | Relevant | Gambar menampilkan gagang kayu berthearding/ulir untuk perkakas pembersih (sapu/pel). Gambar tajam namun terpotong sangat panjang/sempit (aspek rasio ekstrem 432x65 px). Cocok untuk inventaris kebersihan asrama. | Manual Review |
| `prod_0583` | Outvita 7FT Garden Arch Arbor with Seating, Heavy Duty Metal Arbour Archway... | Product Photo (Isolated) | Yes | Good | Irrelevant | Gambar sangat jelas menampilkan gerbang lengkung taman (garden arbor) berbahan besi dengan bangku duduk berhias bunga untuk pesta/taman luar ruang. Tidak relevan untuk inventaris kamar/fasilitas standar asrama mahasiswa. | Exclude |
| `prod_0659` | Elements Ultimate Thin Single Wide Rolling Papers (Display of 25) | Product Photo (Packaging) | Yes | Good | Irrelevant | Gambar jelas menampilkan kotak display kemasan kertas linting rokok (rolling papers). Merupakan produk konsumsi/aksesori rokok, tidak relevan dan bertentangan dengan kebutuhan inventaris asrama. | Exclude |
| `prod_0792` | Big Green Egg SpeediClean™ Palmyra Bristle Long-Handle Grid Scrubber | Product Photo (Isolated) | Yes | Good | Relevant | Gambar jelas menampilkan sikat pembersih panggangan/grill bergagang panjang warna hijau dengan latar belakang putih. Sangat relevan untuk perlengkapan dapur bersama/area BBQ asrama. | Keep |
| `prod_0802` | Brush Research Mfg. - 1-1/4" Diam Helical Steel Tube Brush... | Product Photo (Isolated) | Yes | Good | Maybe Relevant | Gambar menampilkan sikat kawat pembersih tabung/pipa industri pada latar belakang putih. Relevan untuk pemeliharaan fasilitas teknis asrama (maintenance/plumbing), tetapi bukan inventaris umum kamar mahasiswa. | Manual Review |
| `prod_0008` | SOG SEAL XR 3.9" Folding Pocket Knife (Blackout) | Product Photo (Isolated) | Yes | Good | Irrelevant | Gambar jelas menampilkan pisau lipat taktis hitam (folding pocket knife) pada latar belakang putih. Pisau saku/taktis bukan merupakan inventaris resmi asrama dan berpotensi melanggar regulasi keamanan asrama. | Exclude |
| `prod_0273` | Sioux Tools - 1/4" Bit Holder, 700 RPM, Pistol Grip Handle Air Screwdriver... | Product Photo (Isolated) | Yes | Good | Maybe Relevant | Gambar jelas menampilkan obeng pneumatik bertenaga angin berdesain pistol grip (merah-hitam). Relevan untuk perkakas bengkel perawatan/teknisi asrama, bukan inventaris kamar. | Manual Review |
| `prod_0238` | TRUSCO 防振パット 耐熱耐油性 シートタイプ 300X300X10 OH10CR トラスコ | Product Photo (Isolated) | Yes | Good | Relevant | Gambar menampilkan bantalan peredam getaran hitam bergelombang (anti-vibration pad). Berguna untuk meredam getaran mesin cuci, kulkas, atau peralatan di fasilitas asrama. | Keep |
| `prod_0394` | Nintendo Switch Power Cable | Product Photo (Isolated) | Yes | Good | Relevant | Gambar jelas menampilkan adaptor daya (power cable/charger). Relevan sebagai aksesoris elektronik / fasilitas ruang rekreasi asrama atau barang elektronik umum mahasiswa. | Keep |
| `prod_0751` | BCD436HP Uniden Police Scanner (SC) | Diagram / Technical Drawing | Yes | Good | Irrelevant | Gambar adalah diagram/infografis produk pemindai radio polisi genggam (police scanner) beranotasi lengkap dengan garis penunjuk dan label teks fungsi tombol. Bersifat terlalu spesifik/radio hobi dan tidak relevan untuk asrama. | Exclude |
| `prod_0892` | Phoenix Contact 1702018 | Product Photo (Isolated) | Yes | Good | Irrelevant | Gambar menampilkan blok terminal konektor PCB elektronik industri (Phoenix Contact). Komponen elektronik murni, tidak relevan untuk inventaris asrama. | Exclude |
| `prod_0235` | Tischaufsteller fürs Mikrofon Newskill NS-AC-KALIOPE LED Schwarz | Product Photo (Isolated) | Yes | Good | Relevant | Gambar jelas menampilkan mikrofon meja dengan tripod stand dan lampu LED hitam. Sangat relevan untuk perlengkapan meja belajar/podium ruang belajar asrama. | Keep |
| `prod_0741` | Shaker Cinder 24" W x 36" H Wall Diagonal Glass Door Corner Cabinet... | Diagram / Technical Drawing | Yes | Good | Relevant | Gambar merupakan sketsa/garis gambar teknik (blueprint diagram dimensi beranotasi ukuran) lemari kabinet sudut dinding. Produknya relevan (lemari kabinet asrama), namun gambarnya berupa diagram teknis bukan foto produk/furnitur realistik. | Manual Review |
| `prod_0474` | 4 Tier Bookshelf, Bookcase, Etagere, Corner, For Office, Contemporary & Modern | Lifestyle Photo | Yes | Good | Relevant | Foto lingkungan interior (lifestyle room shot) yang jelas menampilkan rak buku sudut 4 tingkat di samping jendela dan sofa ruang tamu/kamar. Sangat relevan untuk perabot kamar tidur/ruang belajar asrama. | Keep |
| `prod_0672` | Safety 1st Pathways Home 2-piece Set, Highchair and Bassinet | Product Photo (Isolated) | Yes | Good | Irrelevant | Gambar jelas menampilkan kursi makan bayi tinggi (highchair) dan ranjang bayi pada latar belakang putih. Merupakan perabot bayi/anak kecil, tidak relevan untuk asrama mahasiswa/pekerja. | Exclude |
| `prod_0510` | Ralis White & Oak Kitchen Cupboard - 5 Door | Lifestyle Photo | Yes | Good | Relevant | Foto interior ruangan dapur (lifestyle shot) yang sangat jelas menampilkan lemari dapur (cupboard) putih berpadu kayu di samping meja makan dan microwave. Sangat relevan untuk fasilitas dapur asrama. | Keep |
| `prod_0054` | FORMAX FD 262 Single-Head Tabber | Product Photo (Isolated) | Yes | Good | Irrelevant | Gambar menampilkan mesin tabber industri berat untuk pemrosesan surat/dokumen massal. Mesin kantor industri berat tidak relevan untuk inventaris standar asrama. | Exclude |
| `prod_0786` | Ultimate Office Mesh Wall File Organizer, 12 Tier Vertical Mount... | Product Photo (Isolated) | Yes | Good | Relevant | Gambar produk jelas menampilkan rak gantung dinding organizer dokumen 12 tingkat dengan inset tangan memasukkan map dokumen berwarna pada latar belakang putih. Sangat relevan untuk kantor administrasi asrama maupun meja belajar. | Keep |
| `prod_0719` | STAPLER-HEAVY DUTY BOSTITCH 65 PREMIUM | Product Photo (Isolated) | Yes | Good | Relevant | Gambar produk terisolasi pada latar putih menampilkan stapler heavy duty hitam. Sangat relevan untuk perlengkapan kantor/ruang belajar asrama. | Keep |
| `prod_0064` | PATIKIL 6 Pcs Desk Call Bell 2.5" Dia with Metal Anti-Rust Construction Blue/White | Product Photo (Isolated) | Yes | Good | Relevant | Gambar produk terisolasi pada latar putih menampilkan susunan 6 buah bel meja logam warna biru-putih. Relevan untuk meja resepsionis/front desk asrama atau meja layanan bersama. | Keep |

---

## 2. Ringkasan Statistik Penilaian

### A. Visual Match (Kesesuaian Visual dengan Judul)
- **Yes:** 20 (100.0%)
- **No:** 0 (0.0%)
- **Unclear:** 0 (0.0%)
> *Catatan cakupan klaim: Kesesuaian visual 100% ini terbukti dan dibatasi pada 20 sampel pilot yang telah diperiksa langsung. Klaim ini tidak menggeneralisasi seluruh dataset sebelum sampel lainnya divalidasi.*

### B. Image Type (Distribusi Tipe Gambar)
- **Product Photo (Isolated):** 15 (75.0%) — Foto produk tunggal atau set produk terisolasi pada latar belakang putih/netral (`prod_0569`, `prod_0583`, `prod_0792`, `prod_0802`, `prod_0008`, `prod_0273`, `prod_0238`, `prod_0394`, `prod_0892`, `prod_0235`, `prod_0672`, `prod_0054`, `prod_0786`, `prod_0719`, `prod_0064`).
- **Lifestyle Photo:** 2 (10.0%) — Foto produk dalam konteks ruangan/interior aktual (`prod_0474`, `prod_0510`).
- **Diagram / Technical Drawing:** 2 (10.0%) — Gambar sketsa blueprint dimensi teknis (`prod_0741`) dan diagram infografis komponen tombol produk (`prod_0751`).
- **Product Photo (Packaging):** 1 (5.0%) — Foto kemasan kotak display retail produk (`prod_0659`).
> *Total: Tepat 20 produk (100.0%). Setiap produk memiliki tepat satu kategori image_type.*

### C. Image Quality (Kualitas Visual Gambar)
- **Good:** 19 (95.0%)
- **Fair:** 1 (5.0%) — `prod_0569` (aspek rasio sangat sempit/panjang, 432x65 px)
- **Poor:** 0 (0.0%)

### D. Dorm Inventory Relevance (Relevansi Inventaris Asrama)
- **Relevant:** 10 (50.0%)
- **Maybe Relevant:** 3 (15.0%)
- **Irrelevant:** 7 (35.0%)

### E. Recommended Action
- **Keep:** 9 (45.0%)
- **Manual Review:** 4 (20.0%)
  - `prod_0569`: Gagang kayu (aspek rasio ekstrem).
  - `prod_0741`: Lemari kabinet (gambar berupa sketsa blueprint/diagram dimensi teknik, bukan foto produk).
  - `prod_0802`: Sikat tabung baja (alat maintenance teknis asrama).
  - `prod_0273`: Obeng angin pneumatik (alat bengkel maintenance asrama).
- **Exclude:** 7 (35.0%)
  - Produk di luar lingkup asrama: `prod_0583` (garden wedding arbor), `prod_0659` (rolling papers rokok), `prod_0008` (pisau lipat taktis), `prod_0751` (diagram scanner polisi), `prod_0892` (komponen PCB), `prod_0672` (perlengkapan bayi), `prod_0054` (mesin industri surat).
