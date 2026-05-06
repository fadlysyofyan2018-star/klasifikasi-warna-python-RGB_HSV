import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# === 1. Dataset Laptop (Contoh Sederhana) ===
data = {
    'Model': ['Aspire 5', 'ROG Strix', 'MacBook Air', 'ThinkPad X1', 'HP Pavilion'],
    'Merek': ['Acer', 'Asus', 'Apple', 'Lenovo', 'HP'],
    'Prosesor': ['Intel i5', 'Intel i7', 'Apple M1', 'Intel i7', 'Intel i5'],
    'RAM': [8, 16, 8, 16, 8],
    'Storage': [512, 1000, 256, 512, 512],
    'GPU': ['Intel UHD', 'NVIDIA RTX 3060', 'Apple GPU', 'Intel Iris Xe', 'Intel UHD'],
    'Harga': [7000000, 20000000, 15000000, 18000000, 8000000],
    'Kategori': ['Kerja', 'Gaming', 'Desain', 'Kerja', 'Kerja']
}

df = pd.DataFrame(data)

# === 2. Fungsi Pencarian Berdasarkan Nama Laptop ===
def cari_spesifikasi(nama_laptop):
    hasil = df[df['Model'].str.lower() == nama_laptop.lower()]
    
    if hasil.empty:
        return None, f"\n❌ Laptop dengan nama '{nama_laptop}' tidak ditemukan dalam database."
    
    laptop = hasil.iloc[0]
    output = (
        f"\n✅ Spesifikasi Laptop '{laptop['Model']}':\n"
        f"- Merek: {laptop['Merek']}\n"
        f"- Prosesor: {laptop['Prosesor']}\n"
        f"- RAM: {laptop['RAM']} GB\n"
        f"- Storage: {laptop['Storage']} GB SSD\n"
        f"- GPU: {laptop['GPU']}\n"
        f"- Kategori: {laptop['Kategori']}\n"
        f"- Harga: Rp{laptop['Harga']:,}"
    )
    return laptop, output

# === 3. Fungsi Rekomendasi Laptop Lebih Bagus ===
def rekomendasi_lebih_bagus(laptop_input):
    # Filter laptop dengan RAM, Storage, dan Harga lebih tinggi
    df_filtered = df[
        (df['RAM'] >= laptop_input['RAM']) &
        (df['Storage'] >= laptop_input['Storage']) &
        (df['Harga'] > laptop_input['Harga']) &
        (df['Model'] != laptop_input['Model'])  # Hindari merekomendasikan laptop yang sama
    ]
    
    if df_filtered.empty:
        return "\n⚠️ Tidak ada rekomendasi laptop yang lebih bagus dari spesifikasi tersebut."
    
    rekomendasi = df_filtered.sort_values(by=['RAM', 'Storage', 'Harga'], ascending=False).iloc[0]
    output = (
        f"\n🔎 Rekomendasi Laptop Lebih Bagus:\n"
        f"- Model: {rekomendasi['Model']}\n"
        f"- Merek: {rekomendasi['Merek']}\n"
        f"- Prosesor: {rekomendasi['Prosesor']}\n"
        f"- RAM: {rekomendasi['RAM']} GB\n"
        f"- Storage: {rekomendasi['Storage']} GB SSD\n"
        f"- GPU: {rekomendasi['GPU']}\n"
        f"- Kategori: {rekomendasi['Kategori']}\n"
        f"- Harga: Rp{rekomendasi['Harga']:,}"
    )
    return output

# === 4. Input dari Pengguna ===
nama = input("Masukkan nama laptop yang ingin dicari: ")
laptop, spesifikasi = cari_spesifikasi(nama)

if laptop is None:
    print(spesifikasi)
else:
    print(spesifikasi)
    print(rekomendasi_lebih_bagus(laptop))
