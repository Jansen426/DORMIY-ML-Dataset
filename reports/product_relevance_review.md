# Product Relevance Review - Sistem Inventaris Gudang Asrama (DORMIY)

**Dokumen Evaluasi dan Rekomendasi Awal Relevansi Kategori Produk**
- **Proyek:** DORMIY (Sistem Pencarian & Rekomendasi Inventaris Asrama RTB)
- **Dataset Sumber:** `data/raw/shopify_sample_1000.csv` (Total: 1000 produk)
- **Tujuan:** Memberikan tinjauan komprehensif seluruh 20 kategori utama beserta contoh konkret produk untuk memandu tim sebelum menentukan aturan filtering dan pembersihan data (Data Cleaning).

> [!NOTE]
> Dokumen ini hanya berisi analisis dan rekomendasi awal. **Tidak ada data yang dihapus, difilter, atau diubah** pada tahap ini.

## 1. Ringkasan Distribusi & Rekomendasi Relevansi Kategori

| No | Kategori Utama | Jumlah Produk | Proporsi (%) | Rekomendasi Awal | Justifikasi Kebutuhan Asrama |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | Home & Garden | 160 | 16.0% | **Relevant** | Mencakup peralatan dapur, kebersihan, perlengkapan makan, wadah penyimpanan, dekorasi asrama, dan perawatan halaman. |
| 2 | Sporting Goods | 148 | 14.8% | **Maybe Relevant** | Fasilitas olahraga dan kegiatan luar ruangan penghuni asrama (bola, peralatan kebugaran/gym), namun beberapa alat khusus (pancing) kurang umum. |
| 3 | Arts & Entertainment | 120 | 12.0% | **Maybe Relevant** | Mencakup alat musik bersama, peralatan prakarya, kanvas/kain kegiatan asrama, stand buku musik, namun beberapa barang dekoratif murni kurang prioritas. |
| 4 | Hardware | 89 | 8.9% | **Relevant** | Sangat esensial untuk perkakas pemeliharaan fasilitas asrama, perbaikan inventaris, kunci, engsel, pisau kerja, dan perbaikan gedung. |
| 5 | Vehicles & Parts | 60 | 6.0% | **Irrelevant** | Suku cadang mesin mobil, komponen otomotif berat, pengapian kendaraan pribadi di luar ruang lingkup inventaris gudang asrama. |
| 6 | Electronics | 57 | 5.7% | **Relevant** | Komponen kelistrikan asrama, adaptor daya, kabel, display, lampu penerangan, dan suku cadang perangkat elektronik fasilitas bersama. |
| 7 | Health & Beauty | 51 | 5.1% | **Maybe Relevant** | Dapat relevan untuk persediaan P3K asrama, sabun/kebersihan bersama, namun sebagian besar berupa kosmetik atau perawatan personal individual. |
| 8 | Business & Industrial | 48 | 4.8% | **Maybe Relevant** | Beberapa perlengkapan keselamatan kerja, labeler industri, atau alat gudang relevan, namun mesin industri besar tidak sesuai. |
| 9 | Apparel & Accessories | 46 | 4.6% | **Irrelevant** | Pakaian pribadi, topi, busana fashion, dan aksesoris personal penghuni (bukan barang inventaris gudang asrama yang dipinjamkan/dikelola bersama). |
| 10 | Animals & Pet Supplies | 46 | 4.6% | **Irrelevant** | Perlengkapan hewan peliharaan (umumnya asrama melarang atau tidak mengelola inventaris pemeliharaan hewan peliharaan). |
| 11 | Food, Beverages & Tobacco | 36 | 3.6% | **Irrelevant** | Bahan makanan segar/olahan, kudapan, dan konsumsi habis pakai individual yang bukan merupakan aset inventaris gudang pencarian alat. |
| 12 | Furniture | 32 | 3.2% | **Relevant** | Perabot langsung untuk kamar santri/mahasiswa asrama, ruang belajar, dan dapur (meja, bangku, lemari kabinet, rak). |
| 13 | Baby & Toddler | 25 | 2.5% | **Irrelevant** | Perlengkapan bayi, popok, pompa ASI, dan kereta bayi tidak relevan dengan lingkungan fasilitas asrama umum. |
| 14 | Toys & Games | 23 | 2.3% | **Maybe Relevant** | Permainan papan (board games) atau hiburan ruang santai bersama asrama, namun mainan anak kecil/bayi kurang relevan. |
| 15 | Cameras & Optics | 22 | 2.2% | **Maybe Relevant** | Dapat digunakan untuk inventaris dokumentasi asrama, kegiatan humas/media, lensa pembesar, atau sistem pengawasan dasar. |
| 16 | Office Supplies | 20 | 2.0% | **Relevant** | Kebutuhan operasional kantor pengelola asrama, administrasi, ATK, papan tulis, bel meja, dan perlengkapan pengorganisasian. |
| 17 | Software | 8 | 0.8% | **Irrelevant** | Lisensi perangkat lunak digital dan file non-fisik yang tidak sesuai dengan sistem inventaris fisik gudang asrama DORMIY. |
| 18 | Services | 4 | 0.4% | **Irrelevant** | Jasa tenaga kerja, instalasi atap, perbaikan baterai (bukan barang fisik yang dicari/direkomendasikan dalam inventaris). |
| 19 | Media | 3 | 0.3% | **Irrelevant** | Rekaman siaran radio atau media non-fisik / karya cetak individual spesifik. |
| 20 | Luggage & Bags | 2 | 0.2% | **Maybe Relevant** | Tas penyimpanan inventaris, tas ransel darurat asrama, atau kantong perlengkapan bepergian/kegiatan luar asrama. |

### Rekapitulasi Pengelompokan Kategori:
- **Relevant:** 5 kategori (358 produk / 35.8%)
- **Maybe Relevant:** 7 kategori (414 produk / 41.4%)
- **Irrelevant:** 8 kategori (228 produk / 22.8%)

---

## 2. Tinjauan Detail dan Contoh Sampel per Kategori Utama

Berikut adalah rincian masing-masing dari 20 kategori utama beserta maksimal 5 contoh produk nyata dari dataset mentah:

### 1. Home & Garden
- **Jumlah Produk:** 160 (16.0% dari dataset)
- **Rekomendasi Relevansi:** `Relevant`
- **Catatan Evaluasi:** Mencakup peralatan dapur, kebersihan, perlengkapan makan, wadah penyimpanan, dekorasi asrama, dan perawatan halaman.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0001]` Airplane Piggy Bank**
   - **Kategori Lengkap:** `Home & Garden > Decor > Piggy Banks & Money Jars > Piggy Banks`
   - **Deskripsi:** The sweetest gift!
2. **`[prod_0004]` Column capital KK13**
   - **Kategori Lengkap:** `Home & Garden > Kitchen & Dining > Barware > Bottle Caps > Crown Bottle Caps`
   - **Deskripsi:** Elevate your column's beauty with our exquisite Column capital KK13. This decorative element adds sophistication and refinement, transforming your col...
3. **`[prod_0019]` 2018  Autumn Girl**
   - **Kategori Lengkap:** `Home & Garden > Decor > Seasonal & Holiday Decorations > Seasonal Village Sets & Accessories`
   - **Deskripsi:** *Deskripsi tidak tersedia (kosong / NaN)*
4. **`[prod_0024]` DCMASBC1N XR FlexVolt Brushcutter Attachment**
   - **Kategori Lengkap:** `Home & Garden > Lawn & Garden > Outdoor Power Equipment Accessories > Multifunction Outdoor Power Equipment Attachments > Weed Trimmer Attachments`
   - **Deskripsi:** The DEWALT DCMASBC1N XR FlexVolt Brushcutter Attachment has a 20cm blade made of unique DEWALT Steel for fast effective cutting, with 4 tips for effic...
5. **`[prod_0027]` のぼり旗 抽選場 W45×H180cm 金巾[1入]**
   - **Kategori Lengkap:** `Home & Garden > Decor > Seasonal & Holiday Decorations > Japanese Traditional Dolls`
   - **Deskripsi:** サイズ：W45×H180cm 素材：金巾 入数：1枚


### 2. Sporting Goods
- **Jumlah Produk:** 148 (14.8% dari dataset)
- **Rekomendasi Relevansi:** `Maybe Relevant`
- **Catatan Evaluasi:** Fasilitas olahraga dan kegiatan luar ruangan penghuni asrama (bola, peralatan kebugaran/gym), namun beberapa alat khusus (pancing) kurang umum.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0006]` Premier Soccer**
   - **Kategori Lengkap:** `Sporting Goods > Athletics > Soccer`
   - **Deskripsi:** Master the essentials for winning soccer from one of the game's most successful coaches. In Premier Soccer, Michael Parker, the wins leader among acti...
2. **`[prod_0028]` Alpha® T 20 Dog Collar, Dog Tracking Collar**
   - **Kategori Lengkap:** `Sporting Goods > Outdoor Recreation > Hunting & Shooting > Hunting > Hunting Dog Equipment > Hunting Dog Collars`
   - **Deskripsi:** TRACK YOUR PACK No matter what kind of dogs you run or how you hunt, Alpha® T 20 is the slim, rugged and universally sized collar designed to help you...
3. **`[prod_0046]` Bodyworx T-Bar Trainer for Machines**
   - **Kategori Lengkap:** `Sporting Goods > Fitness & General Exercise Equipment > Weight Lifting > Weight Lifting Machine & Exercise Bench Accessories`
   - **Deskripsi:** Key Features T-Bar trainer LBRT10 fits onto L314SR, L315SR, L415SR, L470HR, LU475PC & C516RS. Only applies to 2016 stock. Attaches to the main frame o...
4. **`[prod_0051]` Skateboards Complete 22 Inch Mini Cruiser Retro Skateboard for Kids Boys Youths Beginners**
   - **Kategori Lengkap:** `Sporting Goods > Outdoor Recreation > Skateboarding > Complete Skateboards > Mini-Cruisers`
   - **Deskripsi:** About This Meketec Unique Technology : The strong 3.25 inch trucks with different color with others skateboarder，let you skateboarding slide more dist...
5. **`[prod_0068]` Cable Housing 40"**
   - **Kategori Lengkap:** `Sporting Goods > Outdoor Recreation > Boating & Water Sports > Towed Water Sports > Wakeboarding > Wakeboard Parts`
   - **Deskripsi:** outer casing less cable


### 3. Arts & Entertainment
- **Jumlah Produk:** 120 (12.0% dari dataset)
- **Rekomendasi Relevansi:** `Maybe Relevant`
- **Catatan Evaluasi:** Mencakup alat musik bersama, peralatan prakarya, kanvas/kain kegiatan asrama, stand buku musik, namun beberapa barang dekoratif murni kurang prioritas.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0005]` Conn 62HI Bass Trombone Outfit Independent Valves**
   - **Kategori Lengkap:** `Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Brass Instruments > Trombones > Bass Trombones`
   - **Deskripsi:** Conn 62HI Bass Trombone Outfit Independent Valves
2. **`[prod_0010]` Konper Original Large Music Stand. Compatible with Yamaha PSR/YPT/KB/P/DGX Series Keyboard Music Score Stand, Keyboard Sheet Music Stand with 4 Music Book Clip**
   - **Kategori Lengkap:** `Arts & Entertainment > Hobbies & Creative Arts > Musical Instrument & Orchestra Accessories > Music Stands`
   - **Deskripsi:** *Deskripsi tidak tersedia (kosong / NaN)*
3. **`[prod_0022]` SÚPER FALLEROS  (50)**
   - **Kategori Lengkap:** `Arts & Entertainment > Party & Celebration > Party Supplies > Fireworks & Firecrackers > Firecrackers`
   - **Deskripsi:** Contingut: Caixa de 25 trons. Efecte: Tro 0,30 grams per peça. Nivell: 5/12 Categoria: F2 COMANDES I RECOLLIDES Segons la legislació vigent els produc...
4. **`[prod_0030]` Hand Forged Medieval Battle Axe**
   - **Kategori Lengkap:** `Arts & Entertainment > Hobbies & Creative Arts > Collectibles > Collectible Weapons`
   - **Deskripsi:** A battle axe is an axe specifically designed for combat. Knights often fought with battle axes when they were on foot. The battle axe struck with forc...
5. **`[prod_0032]` AE30M-Ft-01 Audio Signal Indicator, 90dB, 14V, IP34 MOFLASH Signalling**
   - **Kategori Lengkap:** `Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Brass Instruments > Alto & Baritone Horns > Mellophones`
   - **Deskripsi:** MOFLASH SIGNALLING - AE30M-FT-01 - Audio Signal Indicator, Industrial, Low Frequency, 90dB, 450Hz, 14VDC, 30mA, IP34, 35mm Ext. Depth Supply Voltage V...


### 4. Hardware
- **Jumlah Produk:** 89 (8.9% dari dataset)
- **Rekomendasi Relevansi:** `Relevant`
- **Catatan Evaluasi:** Sangat esensial untuk perkakas pemeliharaan fasilitas asrama, perbaikan inventaris, kunci, engsel, pisau kerja, dan perbaikan gedung.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0008]` SOG SEAL XR 3.9" Folding Pocket Knife (Blackout)**
   - **Kategori Lengkap:** `Hardware > Tools > Tool Knives`
   - **Deskripsi:** SOG SEAL XR 3.9" Folding Pocket Knife (Blackout)
2. **`[prod_0013]` PHILIP PN SMS Z 10X7/8**
   - **Kategori Lengkap:** `Hardware > Hardware Accessories > Hardware Fasteners > Screws > Sheet Metal Screws`
   - **Deskripsi:** Brand Name: HILLMAN Callout Size: No. 10 Color: Silver Container Size: Finish: Zinc-Plated Head Type: Pan Length: 7/8 Packaging Type: Boxed Point Type...
3. **`[prod_0021]` Brizo Touch-Clean<sup>®</sup> Square Body Spray 84121-SL**
   - **Kategori Lengkap:** `Hardware > Plumbing > Plumbing Fixture Hardware & Parts > Shower Parts > Bathtub & Shower Jets`
   - **Deskripsi:** Brizo body sprays with Touch-Clean® Technology will surround you in water and engulf you in a fluid state. FEATURES 1/2" rough-in Surface mount Body s...
4. **`[prod_0059]` RENOLD Chain-16B-1BLUE-10FT**
   - **Kategori Lengkap:** `Hardware > Hardware Accessories > Chain, Wire & Rope > Chains`
   - **Deskripsi:** Specifications: Brand RENOLD MPN 16B1X10FT Length 10 Feet Pitch 1 Inch Rows Simplex Weight (kg) 8.39
5. **`[prod_0066]` POWERTEC Miter Saw Stand with Wheels, Collapsible and Portable Tool Stand with Systematic Tool Storage Trays, 330Lbs Load Capacity and Quick-Release Mounting Brackets, Miter Saw Accessories (MT4008)**
   - **Kategori Lengkap:** `Hardware > Tool Accessories > Tool Stands > Saw Stands > Miter Saw Stands`
   - **Deskripsi:** Brand: POWERTEC Features: INCLUDES: (1) Collapsible Miter Saw Stand (Rolling wheels included) FUNCTION: A hassle-free and practical workstation stand...


### 5. Vehicles & Parts
- **Jumlah Produk:** 60 (6.0% dari dataset)
- **Rekomendasi Relevansi:** `Irrelevant`
- **Catatan Evaluasi:** Suku cadang mesin mobil, komponen otomotif berat, pengapian kendaraan pribadi di luar ruang lingkup inventaris gudang asrama.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0012]` 9641620A 4-Piece Kit A/C Compressor, With Clutch, 6-Groove Pulley, 2.4L, 4Cyl, GPD A/C Compressor, Includes (1) A/C Compressor, (1) A/C Expansion Valve, (1) A/C O-Ring and Gasket Seal Kit and (1) A/C Condenser**
   - **Kategori Lengkap:** `Vehicles & Parts > Vehicle Parts & Accessories > Motor Vehicle Parts > Motor Vehicle Climate Control > AC Compressors`
   - **Deskripsi:** Specifications Type A/C Compressor OE number 10670 Quanity sold Sold Individualy Product Fit Direct Fit Vehicle Fit 2011HyundaiSonata(GL) 2011HyundaiS...
2. **`[prod_0014]` Vortex RL210 Black 1 Bar Roof Rack**
   - **Kategori Lengkap:** `Vehicles & Parts > Vehicle Parts & Accessories > Vehicle Storage & Cargo > Motor Vehicle Carrying Racks > Vehicle Cargo Racks`
   - **Deskripsi:** Utilising our highly regarded Vortex bars, this system offers you compatibility with a wide selection of Rhino-Rack accessories. So whether you're a t...
3. **`[prod_0031]` NGK 2016-09 Toyota Venza COP Pencil Type Ignition Coil**
   - **Kategori Lengkap:** `Vehicles & Parts > Vehicle Parts & Accessories > Motor Vehicle Parts > Motor Vehicle Engine Parts > Ignition Components > Ignition Coils`
   - **Deskripsi:** NGK ignition coils are manufactured to meet or exceed OE standards for the highest durability and operational performance, so they can be installed wi...
4. **`[prod_0038]` Hertz HRC BM2**
   - **Kategori Lengkap:** `Vehicles & Parts > Vehicle Parts & Accessories > Motor Vehicle Electronics > Motor Vehicle Speakers > Woofers`
   - **Deskripsi:** Hertz HRC BM2 Bassfjernkontroll For å justere bassnivå. Passer til Hertz Marine Venezia -20 / +6dB justering for å tilpasse bass til personlig referan...
5. **`[prod_0058]` PPS Direct Ignition Coil - Yamaha, Arctic Cat - 36-8409**
   - **Kategori Lengkap:** `Vehicles & Parts > Vehicle Parts & Accessories > Motor Vehicle Parts > Motor Vehicle Engine Parts > Ignition Components > Ignition Coils`
   - **Deskripsi:** FEATURES Direct OEM-style replacement. Pure copper windings prevent internal shorts and dielectric failure. High-dielectric moldings pulled into vacuu...


### 6. Electronics
- **Jumlah Produk:** 57 (5.7% dari dataset)
- **Rekomendasi Relevansi:** `Relevant`
- **Catatan Evaluasi:** Komponen kelistrikan asrama, adaptor daya, kabel, display, lampu penerangan, dan suku cadang perangkat elektronik fasilitas bersama.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0007]` Vishay LED Displays TDSG1160**
   - **Kategori Lengkap:** `Electronics > Components`
   - **Deskripsi:** Vishay, TDSG1160 Vishay 7-Segment LED Display, CC Green 6 mcd RH DP 7mm
2. **`[prod_0009]` Florida Gators PS5 VarsityWrapz**
   - **Kategori Lengkap:** `Electronics > Video Game Console Accessories > Home Game Console Accessories > Home Game Console Skins`
   - **Deskripsi:** Florida Gators PS5 Console Skin Officially licensed Florida Gators PS5 wrap – precision fit, vibrant orange and blue design, and durable vinyl protect...
3. **`[prod_0015]` 3pcs LM317 DC-DC Converter Buck Step Down Module Linear Regulator Adjustable Voltage Regulator Power Supply Board**
   - **Kategori Lengkap:** `Electronics > Circuit Boards & Components`
   - **Deskripsi:** Feature: Output Current: 1.5A (minimum), 2.2A (typ) Input and output voltage difference (VI-VO): 40Vdc (max) Adjustable output voltage range: 1.2 ~ 37...
4. **`[prod_0037]` GT-Lite inkl. Vibrationsmotoren**
   - **Kategori Lengkap:** `Electronics > Arcade Equipment > Video Game Arcade Cabinet Accessories > Joysticks`
   - **Deskripsi:** Eigenschaften: Originalgetreuer Rennsitz: Unser Premium-Schalensitz aus Fiberglas wurde exklusiv für GT-Rennen entwickelt und spiegelt das Erlebnis ei...
5. **`[prod_0061]` ACR39U-NF PocketMate II USB-C Smart Card Reader**
   - **Kategori Lengkap:** `Electronics > Electronics Accessories > Computer Components > Input Devices > Electronic Card Readers`
   - **Deskripsi:** ACR39 PocketMate II with USB Type C Connector represents an ACS new paradigm. No larger than a USB stick, this smart card reader is capable of support...


### 7. Health & Beauty
- **Jumlah Produk:** 51 (5.1% dari dataset)
- **Rekomendasi Relevansi:** `Maybe Relevant`
- **Catatan Evaluasi:** Dapat relevan untuk persediaan P3K asrama, sabun/kebersihan bersama, namun sebagian besar berupa kosmetik atau perawatan personal individual.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0002]` PostuEase™ - Justerbart hållningsbälte för ryggen**
   - **Kategori Lengkap:** `Health & Beauty > Personal Care > Back Care`
   - **Deskripsi:** Förändra din hållning, lindra smärta och återfå självförtroendet! Orsakar sned rygg obehag och påverkar ditt självförtroende? Längtar du efter en lösn...
2. **`[prod_0043]` 2PCS Retainer Case with Mirror and Adjustable Vent Holes, Cute Slim Aligner Case Compatible with Invisalign, Night Mouth Guard Case, With Retainer Remover Tool, Chew & Brush, White+White**
   - **Kategori Lengkap:** `Health & Beauty > Personal Care > Oral Care > Orthodontic Appliance Cases > Soft Orthodontic Appliance Cases`
   - **Deskripsi:** Brand: Heigoeost Color: Round: White+White Features: PORTABLE RETAINER CASE WITH MAGNETIC CLOSE - These travel retainer cases are 3.15 in diameter × 1...
3. **`[prod_0062]` Nepro HP Strawberry (220ml)**
   - **Kategori Lengkap:** `Health & Beauty > Health Care > Fitness & Nutrition > Tube Feeding Supplements`
   - **Deskripsi:** Nepro HP Nepro HP is a 1.8kcal/ml, energy dense, oral nutritional supplement and tube feed, for use as a sole source of nutrition or as a nutritional...
4. **`[prod_0067]` Tanning Dead Skin Remover 100 ml ( Pack of 2 )**
   - **Kategori Lengkap:** `Health & Beauty > Personal Care > Cosmetics > Skin Care > Body Oil`
   - **Deskripsi:** *Deskripsi tidak tersedia (kosong / NaN)*
5. **`[prod_0093]` MelodySusie Portable Electric Nail Drill,PC120B Compact Efile Electrical Professional Nail File Kit for Acrylic, Gel Nails, Manicure Pedicure Polishing Shape Tools Design for Home Salon Use, Gold**
   - **Kategori Lengkap:** `Health & Beauty > Personal Care > Cosmetics > Cosmetic Tools > Nail Tools > Nail Drills`
   - **Deskripsi:** About This PC120B Multifunctional: Designed with 6 kinds of metal bits (also works with all kinds of 3/32" shank bits) and 6 sanding bands, which are...


### 8. Business & Industrial
- **Jumlah Produk:** 48 (4.8% dari dataset)
- **Rekomendasi Relevansi:** `Maybe Relevant`
- **Catatan Evaluasi:** Beberapa perlengkapan keselamatan kerja, labeler industri, atau alat gudang relevan, namun mesin industri besar tidak sesuai.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0011]` HP1044 SAUER TUROLLA PUMP**
   - **Kategori Lengkap:** `Business & Industrial > Mining & Quarrying > Mining & Quarrying Machinery > Crushers > Cone Crushers`
   - **Deskripsi:** HP1044 Hydraulic pump is an original Danfoss© part produced in Germany. It has been engineered to superior standards, and is compatible with Sandvik©...
2. **`[prod_0077]` Boston Gear - 2.06 Centerline Distance, 60:1, 1/2 Input Horsepower, 670 Lbs. Max Torque, Speed Reducer - 56C NEMA**
   - **Kategori Lengkap:** `Business & Industrial > Heavy Machinery > Excavators > Dragline Excavators`
   - **Deskripsi:** Item #: 05896840 Brand: Boston Gear Model #: 63053 Exact Tooling IR#: 04 Product Specifications Centerline Distance (Decimal Inch) 2.060 Ratio 60:1 NE...
3. **`[prod_0088]` Flask, PC, 1 L, No Baffle, VersaCap 50, Non-Sterile**
   - **Kategori Lengkap:** `Business & Industrial > Science & Laboratory > Laboratory Supplies > Laboratory Flasks > Erlenmeyer Laboratory Flasks`
   - **Deskripsi:** Erlenmeyer Flask With 53B Cap, Not Sterile Foxx Life Science EZ clear® Erlenmeyer Shaker Flasks are molded from virgin, optically clear, non-leaching...
4. **`[prod_0089]` BUCK Scientific 1-Q-20 Type 1 Quartz Cuvette path length : 20mm with Warranty**
   - **Kategori Lengkap:** `Business & Industrial > Science & Laboratory > Laboratory Equipment > Spectrometer Accessories > Cuvettes`
   - **Deskripsi:** BUCK Scientific 1-Q-20 Type 1 Quartz Cuvette path length : 20mm with Warranty Note: For all International Orders, the buyer will be solely responsible...
5. **`[prod_0092]` Vacuum Sealing Assembly for 50mm Tube w/ KF-25 Port & 1/4" Feedthrough - FL-50KF25-FT (D/M)**
   - **Kategori Lengkap:** `Business & Industrial > Science & Laboratory > Laboratory Equipment > Laboratory Ovens`
   - **Deskripsi:** This is a pair of smart sealing assembly for 2" vacuum tube furnace to seal both ends of 50 +/- 1.0 mm tube without any welding and gluing. SPECIFICAT...


### 9. Apparel & Accessories
- **Jumlah Produk:** 46 (4.6% dari dataset)
- **Rekomendasi Relevansi:** `Irrelevant`
- **Catatan Evaluasi:** Pakaian pribadi, topi, busana fashion, dan aksesoris personal penghuni (bukan barang inventaris gudang asrama yang dipinjamkan/dikelola bersama).

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0003]` Panama Man**
   - **Kategori Lengkap:** `Apparel & Accessories > Clothing Accessories > Hats > Panama Hats`
   - **Deskripsi:** Description The refined tradition of Italian tailoring by 100% Capri meets the sophisticated elegance of French craftsmanship in the creation of the i...
2. **`[prod_0017]` Cargo Trouser Pants**
   - **Kategori Lengkap:** `Apparel & Accessories > Clothing > Pants > Cargo Pants`
   - **Deskripsi:** These Cargo Trouser Pants offer a practical and stylish solution for your everyday wardrobe. Featuring multiple pockets for convenient storage, these...
3. **`[prod_0018]` Maternity Maxi Copper Tencel Panel Skirt**
   - **Kategori Lengkap:** `Apparel & Accessories > Clothing > Maternity Clothing > Maternity Skirts`
   - **Deskripsi:** Ladies maxi maternity copper tencel panel skirt with wide adjustable elastic waistband. ֲ Available in the following colors: Midnight Blue Black Compo...
4. **`[prod_0023]` C4M Pouch Enhancing Thong Pearl Extra Large**
   - **Kategori Lengkap:** `Apparel & Accessories > Clothing > Men's Undergarments > Men's Underwear > Thongs`
   - **Deskripsi:** As the name implies the Cut4Men Enhanced Thong offers you unmatched comfort thanks to the ergonomically designed front pouch to enhance your manhood g...
5. **`[prod_0050]` In My Pregnant Era 2 Sides Shirt, Pregnancy Sweatshirt, Gift for New Mom, Pregnant Women Tee, Baby Reveal Gift, Mother's Day Gift, Cute New Mom Tee**
   - **Kategori Lengkap:** `Apparel & Accessories > Clothing > Maternity Clothing > Maternity Tops > T-Shirts`
   - **Deskripsi:** 🔥 Welcome to Our Store! Explore our collection of T-Shirts, Hoodies, and Sweatshirts , designed for ultimate comfort and everyday style. ✨ Why You'll...


### 10. Animals & Pet Supplies
- **Jumlah Produk:** 46 (4.6% dari dataset)
- **Rekomendasi Relevansi:** `Irrelevant`
- **Catatan Evaluasi:** Perlengkapan hewan peliharaan (umumnya asrama melarang atau tidak mengelola inventaris pemeliharaan hewan peliharaan).

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0129]` Gourde pour Chien – Hydratation facile, partout et à tout moment**
   - **Kategori Lengkap:** `Animals & Pet Supplies > Pet Supplies > Pet Bowls, Feeders & Waterers > Travel Bowls`
   - **Deskripsi:** Ne laissez plus votre chien manquer d’eau lors de vos balades, randonnées ou voyages grâce à notre gourde pour chien , spécialement conçue pour offrir...
2. **`[prod_0210]` PawHut 5pc Dog Agility Training Equipment Set with Spray Water Tube, White**
   - **Kategori Lengkap:** `Animals & Pet Supplies > Pet Supplies > Pet Agility Equipment`
   - **Deskripsi:** Highlights - Complete Dog Agility Set: Enhance your dog's agility, speed, and obedience. This 3-piece dog agility training equipment set includes an a...
3. **`[prod_0254]` PAWZIDEA Double Pet Stroller with 2 Detachable Carriers, Portable Dog Crate for Car Travel & TSA-Approved Expandable Cat Carrier, Foldable Lightweight Jogger Stroller for 2–4 Cats or Small/Medium Dogs**
   - **Kategori Lengkap:** `Animals & Pet Supplies > Pet Supplies > Pet Strollers > Double-Decker Strollers`
   - **Deskripsi:** About This 4-in-1 Multifunctional Double-Decker Design – Fits 2–4 cats or 2 small dogs with a bottom TSA-approved expandable carrier (18″ × 11″ × 11″,...
4. **`[prod_0265]` REPTIZOO Crocodile Skull Hide Cave 29 x 14.5 x 8cm(H) #ERS34L**
   - **Kategori Lengkap:** `Animals & Pet Supplies > Pet Supplies > Reptile & Amphibian Supplies > Reptile & Amphibian Habitats`
   - **Deskripsi:** Product Description: - Made from safe contact materials - Easy to clean one piece design - Hideouts reduce stress on pets and provide easy entrance an...
5. **`[prod_0268]` [ 2 Packs ] Pet Hair Removal Comb Flea Comb, New Cat Brush with Release Button Pet Hair Grooming Brush Supplies (Yellow+Green)**
   - **Kategori Lengkap:** `Animals & Pet Supplies > Pet Supplies > Pet Grooming Supplies > Pet Combs & Brushes > Combs`
   - **Deskripsi:** About This One - Button Self - Cleaning, A Hassle - Free Solution: Bid farewell to the arduous task of cleaning pet hair from brushes. Our Pet Hair Re...


### 11. Food, Beverages & Tobacco
- **Jumlah Produk:** 36 (3.6% dari dataset)
- **Rekomendasi Relevansi:** `Irrelevant`
- **Catatan Evaluasi:** Bahan makanan segar/olahan, kudapan, dan konsumsi habis pakai individual yang bukan merupakan aset inventaris gudang pencarian alat.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0020]` Mithai & More Thabdi Penda 250 gms And 500 gms**
   - **Kategori Lengkap:** `Food, Beverages & Tobacco > Food Items > Prepared Foods`
   - **Deskripsi:** A must try milk-based fudge, our succulent Thabdi Penda makes for a luxurious treat. Originating from Saurashtra, Gujarat, Thabdi Penda is an Indian s...
2. **`[prod_0045]` Coentros**
   - **Kategori Lengkap:** `Food, Beverages & Tobacco > Food Items > Fruits & Vegetables > Fresh & Frozen Vegetables > Parsley Roots`
   - **Deskripsi:** Preço por meio quilo
3. **`[prod_0052]` HALDIRAM S GULABJAMUN 1KG**
   - **Kategori Lengkap:** `Food, Beverages & Tobacco > Food Items > Prepared Foods`
   - **Deskripsi:** HALDIRAM S GULABJAMUN 1KG - '8904004405910
4. **`[prod_0158]` GREEN VALLEY CREAMERY SOUR CREAM LCF ORG - 12 OZ**
   - **Kategori Lengkap:** `Food, Beverages & Tobacco > Food Items > Dairy Products > Sour Cream`
   - **Deskripsi:** Discover this high-quality product, designed to meet your everyday needs. Made with natural and wholesome ingredients, this item offers exceptional va...
5. **`[prod_0211]` Tayto Mega Meanies Pickled Onion Flavour. 35g**
   - **Kategori Lengkap:** `Food, Beverages & Tobacco > Food Items > Snack Foods > Puffed Rice Cakes`
   - **Deskripsi:** Tayto Mega Meanies Pickled Onion, a childhood favourite that has stood the test of time. These crunchy puffed corn snacks are a nostalgic delight, dus...


### 12. Furniture
- **Jumlah Produk:** 32 (3.2% dari dataset)
- **Rekomendasi Relevansi:** `Relevant`
- **Catatan Evaluasi:** Perabot langsung untuk kamar santri/mahasiswa asrama, ruang belajar, dan dapur (meja, bangku, lemari kabinet, rak).

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0034]` Anrichte DKD Home Decor natürlich Weiß Mango-Holz (193 x 40,6 x 91,4 cm)**
   - **Kategori Lengkap:** `Furniture > Cabinets & Storage > Buffets`
   - **Deskripsi:** Wenn Sie Ihrem Zuhause einen Hauch von Originalität verleihen möchten, tun Sie dies mit Anrichte DKD Home Decor natürlich Weiß Mango-Holz (193 x 40,6...
2. **`[prod_0069]` HOMCOM End of Bed Bench, Window Seat, Tufted Bench for Bedroom, Hallway, Living Room, Cream White**
   - **Kategori Lengkap:** `Furniture > Benches > Storage & Entryway Benches > Window Seats`
   - **Deskripsi:** Get comfy with this bedroom bench from HOMCOM. Breathable linen-touch fabric and button-tufted detail add vintage glamor to your house. Its compact si...
3. **`[prod_0072]` Cameo Combination Wardrobe - Stone White**
   - **Kategori Lengkap:** `Furniture > Cabinets & Storage > Armoires & Wardrobes`
   - **Deskripsi:** Cameo is a beautiful stone white lacquered bedroom range. Its timeless shaker design is the perfect accompaniment to any interior style and is perfect...
4. **`[prod_0078]` Scaune de grădină cu perne 2 buc Gri deschis Poly Ratan**
   - **Kategori Lengkap:** `Furniture > Outdoor Furniture > Outdoor Seating > Outdoor Chairs > Club Chairs`
   - **Deskripsi:** Relaxați-vă și bucurați-vă de aer liber în aceste scaune confortabile de grădină! Material durabil: Ratanul PE, cunoscut și sub numele de poliratan, e...
5. **`[prod_0090]` Shaker Gray Double Vanity Sink Base Cabinet**
   - **Kategori Lengkap:** `Furniture > Cabinets & Storage > Vanities > Bathroom Vanities > Vanity Bases`
   - **Deskripsi:** Like Cabinets: Factory-Direct RTA Cabinets with Nationwide Inventory and Fast Shipping Like Cabinets offers factory-direct ready-to-assemble (RTA) cab...


### 13. Baby & Toddler
- **Jumlah Produk:** 25 (2.5% dari dataset)
- **Rekomendasi Relevansi:** `Irrelevant`
- **Catatan Evaluasi:** Perlengkapan bayi, popok, pompa ASI, dan kereta bayi tidak relevan dengan lingkungan fasilitas asrama umum.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0016]` Baby Carrier Front Hold Baby Sitting on Lumbar Stool**
   - **Kategori Lengkap:** `Baby & Toddler > Baby Transport > Baby Carriers > Mei Tai Carriers`
   - **Deskripsi:** Color classification: Sakura powder [pure cotton] breathable and comfortable mint blue [pure cotton] breathable and comfortable star blue [pure cotton...
2. **`[prod_0026]` Prince Lionheart My Twist'r Diaper System**
   - **Kategori Lengkap:** `Baby & Toddler > Diapering > Diaper Pails > Diaper Disposal Systems`
   - **Deskripsi:** Prince Lionheart My Twist'r Diaper System Welcome to the new age of diaper disposal – the revolutionary and incredibly user-friendly My Twist’R® Diape...
3. **`[prod_0108]` Crinkle Teether Skippy Snail**
   - **Kategori Lengkap:** `Baby & Toddler > Baby Health > Pacifiers & Teethers`
   - **Deskripsi:** Crinkle Teether Skippy Snail
4. **`[prod_0174]` Vaso de Entrenamiento**
   - **Kategori Lengkap:** `Baby & Toddler > Nursing & Feeding > Sippy Cups`
   - **Deskripsi:** Aprender a beber bebidas puede ser un desafío para tu bebé. Vaso con agarraderas en ambos extremos que lo hacen práctico y más fácil de dominar. Hecho...
5. **`[prod_0207]` Multi-Use Cover - Cody**
   - **Kategori Lengkap:** `Baby & Toddler > Baby Transport Accessories > Shopping Cart & High Chair Covers`
   - **Deskripsi:** * Multi-use 5-in-1 Design * Stretchy fabric fits most all car seats, shopping carts, high chairs and nursing mothers. It can also be a trendy infinity...


### 14. Toys & Games
- **Jumlah Produk:** 23 (2.3% dari dataset)
- **Rekomendasi Relevansi:** `Maybe Relevant`
- **Catatan Evaluasi:** Permainan papan (board games) atau hiburan ruang santai bersama asrama, namun mainan anak kecil/bayi kurang relevan.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0044]` [Pre-order] YaHaHa with LED -ShenYin Studio**
   - **Kategori Lengkap:** `Toys & Games > Toys > Dolls, Playsets & Toy Figures > Puppet Theaters`
   - **Deskripsi:** Studio: ShenYin Studio Product Role: YaHaHa Size:23*18*18CM Price:129USD Deposit:69USD Release date:Q1 2025 Please check the policies on the page befo...
2. **`[prod_0153]` My First Pickle Ball Set**
   - **Kategori Lengkap:** `Toys & Games > Toys > Sports Toys > Racquet Sport Toys`
   - **Deskripsi:** My First Pickle Ball Set
3. **`[prod_0176]` Wind Up Chick Play Toy For Kids**
   - **Kategori Lengkap:** `Toys & Games > Toys > Wind-Up Toys`
   - **Deskripsi:** Bachaa Party brings you the best price for Wind Up Chick Play Toy For Kids with express shipping all over Pakistan. Product Detail: It will surprise k...
4. **`[prod_0224]` E Flite Wing: Viper 64Mm Edf Jet**
   - **Kategori Lengkap:** `Toys & Games > Toys > Remote Control Toys > Remote Control Planes`
   - **Deskripsi:** E Flite Wing: Viper 64mm EDF Jet
5. **`[prod_0261]` Kids Sandbox with Cover, 46' Wooden Sand Box w/Adjustable Canopy, Large Outdoor Cedar Sandpit for Backyard Play**
   - **Kategori Lengkap:** `Toys & Games > Outdoor Play Equipment > Sandboxes`
   - **Deskripsi:** Specifications Place of Origin China Main Color Reddish Brown Main Material Solid Wood Wood Type Hemlock Suitable Age 3 - 8 Years Dangerous Goods #dan...


### 15. Cameras & Optics
- **Jumlah Produk:** 22 (2.2% dari dataset)
- **Rekomendasi Relevansi:** `Maybe Relevant`
- **Catatan Evaluasi:** Dapat digunakan untuk inventaris dokumentasi asrama, kegiatan humas/media, lensa pembesar, atau sistem pengawasan dasar.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0095]` Arista 4-in-1 Enlarging Easel**
   - **Kategori Lengkap:** `Cameras & Optics > Photography > Darkroom > Enlarging Equipment > Darkroom Easels`
   - **Deskripsi:** The Arista 4-in-1 Enlarging Easel is easy to use and very versatile. It is one of the most basic pieces of equipment in almost all darkrooms. It holds...
2. **`[prod_0172]` Oben QR-10 Quick Release Plate**
   - **Kategori Lengkap:** `Cameras & Optics > Camera & Optic Accessories > Tripod & Monopod Accessories`
   - **Deskripsi:** Oben QR-10 Quick Release Plate The Oben QR-10 Quick Release Plate is a camera plate that fits the Arca Swiss- style quick-release element of Oben's BB...
3. **`[prod_0246]` TDM Adapter for MEADE LX200 ACF**
   - **Kategori Lengkap:** `Cameras & Optics > Camera & Optic Accessories > Optic Accessories > Telescope Accessories`
   - **Deskripsi:** Description You do not have to give up your current mount to enjoy the full benefits of a Telescope Drive Master from Explore Scientific. This simple...
4. **`[prod_0248]` Lantern Slide Case and 12 Framed Glass Slides**
   - **Kategori Lengkap:** `Cameras & Optics > Camera & Optic Accessories > Camera Parts & Accessories > Flash Brackets`
   - **Deskripsi:** A set of twelve framed glass slides and wooden case. Approximate dimensions (WxDxH): 11.5"x4"x3.5 " SKU: SJAM0870 Whether you're a collector, looking...
5. **`[prod_0302]` FUJIFILM FT-XH File Transmitter Grip**
   - **Kategori Lengkap:** `Cameras & Optics > Camera & Optic Accessories > Camera Parts & Accessories > Camera Grips > Battery Grips`
   - **Deskripsi:** FUJIFILM FT-XH File Transmitter Grip The FT-XH File Transmitter Grip vastly improves the networking capabilities of the camera. It has fast Wi-Fi conn...


### 16. Office Supplies
- **Jumlah Produk:** 20 (2.0% dari dataset)
- **Rekomendasi Relevansi:** `Relevant`
- **Catatan Evaluasi:** Kebutuhan operasional kantor pengelola asrama, administrasi, ATK, papan tulis, bel meja, dan perlengkapan pengorganisasian.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0054]` FORMAX FD 262 Single-Head Tabber**
   - **Kategori Lengkap:** `Office Supplies > Paper Handling > Paper Folding Machines`
   - **Deskripsi:** The Formax FD 262 Single-Head Tabber makes quick work of applying tabs to folded mailpieces, and is designed to meet all USPS requirements for mailing...
2. **`[prod_0064]` PATIKIL 6 Pcs Desk Call Bell 2.5" Dia with Metal Anti-Rust Construction Blue/White**
   - **Kategori Lengkap:** `Office Supplies > Office Instruments > Call Bells`
   - **Deskripsi:** About this item Material: Metal, Color: Red/White, Overall Size: 6.4 x 4.4 cm / 2.52 x 1.73 inch (Dia*H), Packing List: 2 Pcs x Call Bell Bright Sound...
3. **`[prod_0110]` Quality Park - Mailers, Sheets & Envelopes; Type: Poly Mailer ; Style: Self Adhesive ; Width (Inch): 12 ; Length (Inch): 9 ; Box Quantity: 100 ; Size: 9 x 12**
   - **Kategori Lengkap:** `Office Supplies > Shipping Supplies`
   - **Deskripsi:** Item #: 28807675 Brand: Quality Park Model #: QUA77390 Product Specifications Mailers, Sheets & Envelopes; Type: Poly Mailer ; Style: Self Adhesive ;...
4. **`[prod_0173]` EXTRACTOR DE AIRE**
   - **Kategori Lengkap:** `Office Supplies > Office Equipment`
   - **Deskripsi:** ¿Estás buscando una solución eficiente para mejorar la ventilación en tu lugar de trabajo? ¡Entonces estás en el lugar correcto con nuestro extractor...
5. **`[prod_0198]` Tape Logic - 4-3/4" Long, Black/White Paper D.O.T. Labels - For Multi-Use**
   - **Kategori Lengkap:** `Office Supplies > General Office Supplies > Labels & Tags > Label Tapes & Refill Rolls`
   - **Deskripsi:** Item #: 39584537 Brand: Tape Logic Model #: DL519P2 Exact Tooling IR#: 04 Product Specifications Type D.O.T. Labels Color Black/White For Use With Mul...


### 17. Software
- **Jumlah Produk:** 8 (0.8% dari dataset)
- **Rekomendasi Relevansi:** `Irrelevant`
- **Catatan Evaluasi:** Lisensi perangkat lunak digital dan file non-fisik yang tidak sesuai dengan sistem inventaris fisik gudang asrama DORMIY.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0036]` Software de Automatización Radio**
   - **Kategori Lengkap:** `Software > Computer Software > Multimedia & Design Software > Media Viewing Software`
   - **Deskripsi:** AVRA. Es un software de automatización de radio avanzado con capacidad de reproducción de video HD (720p) y software de mezcla de video de 6 canales c...
2. **`[prod_0202]` Lavender flowers over white wood background**
   - **Kategori Lengkap:** `Software > Digital Goods & Currency > Desktop Wallpapers`
   - **Deskripsi:** Lavender Flowers Over White Wood Background - purple flowers on a white background
3. **`[prod_0304]` Free Cosmetic Concept Mock-Up Psd**
   - **Kategori Lengkap:** `Software > Computer Software > Multimedia & Design Software > Web Design Software`
   - **Deskripsi:** We deliver staggering free mockups that save you time and money and this time we thought to delight you big time with the best free cosmetic concept m...
4. **`[prod_0393]` Free Top View Of Desk With Frame And Pencils Psd**
   - **Kategori Lengkap:** `Software > Digital Goods & Currency > Stock Photographs & Video Footage`
   - **Deskripsi:** Visit Download Page Free Top View Of Desk With Frame And Pencils Psd for any designer that is looking to display their design professionally. Freepik...
5. **`[prod_0397]` Verkada 1-Year Cellular Backup License**
   - **Kategori Lengkap:** `Software > Computer Software > Antivirus & Security Software`
   - **Deskripsi:** Verkada 1-Year Cellular Backup License


### 18. Services
- **Jumlah Produk:** 4 (0.4% dari dataset)
- **Rekomendasi Relevansi:** `Irrelevant`
- **Catatan Evaluasi:** Jasa tenaga kerja, instalasi atap, perbaikan baterai (bukan barang fisik yang dicari/direkomendasikan dalam inventaris).

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0117]` Telhadista**
   - **Kategori Lengkap:** `Services > Building & Construction Services > Specialized Construction Services > Roofing & Guttering`
   - **Deskripsi:** Instalação, reparo e manutenção de telhados de edifícios residenciais e comerciais.
2. **`[prod_0206]` PBP004 Ryobi 18V Lithium Battery Rebuild Service (Upgraded to 5Ah)**
   - **Kategori Lengkap:** `Services > Home Improvement Services > Electrical Services`
   - **Deskripsi:** For the cost of this service we will replace all of the cells in the PBP004 battery that you send to us. Notes: Rebuild capacity is upgraded from 4.0A...
3. **`[prod_0454]` 991.2 M-Tuner ProTune**
   - **Kategori Lengkap:** `Services > Automotive Services > Automotive Electrical Services`
   - **Deskripsi:** We are now offering remote ProTuning for all of our customers who have purchased the M-Tuner Suite for 991.2. For those of you who are looking for eve...
4. **`[prod_0959]` Ultimate Irrigation Contractor Package**
   - **Kategori Lengkap:** `Services > Home Improvement Services > Outdoor Services`
   - **Deskripsi:** Ultimate Irrigation Contractor Package Contractors $2,999.99 + shipping Includes: Lifetime Access to online courses for both Business and Trade portio...


### 19. Media
- **Jumlah Produk:** 3 (0.3% dari dataset)
- **Rekomendasi Relevansi:** `Irrelevant`
- **Catatan Evaluasi:** Rekaman siaran radio atau media non-fisik / karya cetak individual spesifik.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0025]` EDEL RECORDS RADIO STATION PRAVO, PATTY**
   - **Kategori Lengkap:** `Media > Podcasts & Live Streams > Radio Shows`
   - **Deskripsi:** EDEL RECORDS RADIO STATION PRAVO, PATTY Nome dell'articolo: stazione radio Tipologia di prodotto: ABIS_MUSIC Marca: EDEL RECORDS
2. **`[prod_0118]` Red Faces**
   - **Kategori Lengkap:** `Media > Magazines & Newspapers > Newspapers`
   - **Deskripsi:** A red boat and a red bike. North Bondi
3. **`[prod_0821]` Reading Contemporary Electric Bass**
   - **Kategori Lengkap:** `Media > Sheet Music`
   - **Deskripsi:** Book Synopsis (Fretted). This Berklee Workshop is a comprehensive collection of exercises and performance studies designed to expand your bass playing...


### 20. Luggage & Bags
- **Jumlah Produk:** 2 (0.2% dari dataset)
- **Rekomendasi Relevansi:** `Maybe Relevant`
- **Catatan Evaluasi:** Tas penyimpanan inventaris, tas ransel darurat asrama, atau kantong perlengkapan bepergian/kegiatan luar asrama.

**Contoh Produk (Maksimal 5 Sampel):**
1. **`[prod_0432]` Bébé Nomade Pusletaske**
   - **Kategori Lengkap:** `Luggage & Bags > Diaper Bags`
   - **Deskripsi:** Bébé Nomade Rygsækken – Den ultimative alt-i-en løsning for forældre på farten Bébé Nomade rygsækken er skabt med fokus på både bekvemmelighed og komf...
2. **`[prod_0441]` sugar skull Floral Pattern Diaper Bag Backpack**
   - **Kategori Lengkap:** `Luggage & Bags > Diaper Bags`
   - **Deskripsi:** sugar skull Floral Pattern Diaper Bag Backpack Made to Order Item. It is hand-cut and sewn just for your order! This process starts as soon as your or...


---

## 3. Implikasi untuk Tahap Data Cleaning Selanjutnya

1. **Opsi Kebijakan Filtering Tim:**
   - **Opsi Konservatif (Mempertahankan Fleksibilitas):** Tetap memproses 1.000 produk ke data cleaned, namun menambahkan kolom metadata `relevance_category` (`Relevant`, `Maybe Relevant`, `Irrelevant`). Tim NLP/CV dapat memfilter secara modular tanpa kehilangan data asli.
   - **Opsi Spesifik (Penyaringan Ketat Inventaris):** Hanya mengekstrak kategori `Relevant` (358 produk, 35.8%) atau menggabungkan `Relevant + Maybe Relevant` (741 produk, 74.1%), serta mengeliminasi kategori `Irrelevant` (259 produk, 25.9%).
2. **Persetujuan Diperlukan:** Tim diharapkan memeriksa daftar contoh di atas sebelum script filtering / cleaning dieksekusi.
