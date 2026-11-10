from datasets import load_dataset

# Mengambil dataset dengan metode streaming
dataset = load_dataset(
    "Shopify/product-catalogue",
    split="train",
    streaming=True
)

# Mengambil 5 produk pertama
samples = list(dataset.take(5))

# Menampilkan informasi produk
for i, item in enumerate(samples):
    print(f"\nProduk {i+1}")
    print("Nama:", item["product_title"])
    print("Deskripsi:", item["product_description"])
    print("Kategori:", item["ground_truth_category"])
    print("Brand:", item["ground_truth_brand"])
    print("Gambar tersedia:", item["product_image"] is not None)