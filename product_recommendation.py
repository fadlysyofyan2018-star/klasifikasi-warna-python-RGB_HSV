import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# --- LANGKAH 3: Data Produk ---
data = {
    'product_id': [1, 2, 3, 4, 5],
    'name': ['Laptop Gaming LOQ', 'Laptop Gaming Asus TUF', 'Mouse Nirkabel C', 'Keyboard Mekanik D', 'Monitor Gaming E'],
    'category': ['Elektronik', 'Elektronik', 'Aksesoris', 'Aksesoris', 'Elektronik'],
    'description': ['Laptop cepat untuk gaming dengan GPU RTX 3060 dan layar 144Hz.',
                    'Laptop ringan untuk produktivitas kantor dan rapat, baterai tahan lama.',
                    'Mouse ergonomis dengan sensor presisi, cocok untuk penggunaan harian.',
                    'Keyboard dengan switch taktil, lampu RGB, desain kokoh.',
                    'Monitor 27 inci dengan resolusi 4K dan refresh rate 144Hz, warna akurat.']
}
df = pd.DataFrame(data)

# Menggabungkan fitur teks menjadi satu kolom untuk analisis
df['combined_features'] = df['category'] + ' ' + df['description']

# --- LANGKAH 4: Vektorisasi Teks ---
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_features'])

# --- LANGKAH 5: Hitung Kemiripan ---
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# --- LANGKAH 6: Buat Fungsi Rekomendasi (Tidak Berubah) ---
def get_recommendations(product_name, cosine_sim_matrix, data_frame):
    # Cek apakah nama produk ada dalam data
    if product_name not in data_frame['name'].values:
        return f"Error: Produk '{product_name}' tidak ditemukan dalam daftar."

    # Dapatkan indeks produk yang cocok dengan nama
    indices = pd.Series(data_frame.index, index=data_frame['name']).drop_duplicates()
    idx = indices[product_name]

    # Dapatkan skor kemiripan dari semua produk dengan produk target
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))

    # Urutkan produk berdasarkan skor kemiripan secara menurun
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Ambil 3 produk paling mirip (indeks 0 adalah produk itu sendiri)
    sim_scores = sim_scores[1:4]

    # Dapatkan indeks produk yang direkomendasikan
    product_indices = [i[0] for i in sim_scores]

    # Kembalikan nama produk yang direkomendasikan
    return data_frame['name'].iloc[product_indices]

# ====================================================================
# --- FUNGSI PEMILIHAN INTERAKTIF (VERSI LEBIH KEREN DAN AKTIF) ---
# ====================================================================

def interactive_recommendation_selector_v2(data_frame, cosine_sim_matrix):
    """Memungkinkan pengguna memilih produk dari daftar yang tersedia dengan UI konsol yang ditingkatkan."""
    
    product_list = data_frame['name'].tolist()

    # Fungsi internal untuk menampilkan menu
    def display_menu():
        print("\n" + "="*60)
        print("                  SISTEM REKOMENDASI E-COMMERCE ")
        print("="*60)
        print("Pilih produk yang Anda minati untuk mendapatkan rekomendasi serupa:")
        print("-" * 60)
        for i, name in enumerate(product_list):
            print(f"| {i+1:2}. {name:40} |") # Formatting agar lebih rapi
        print("-" * 60)
    
    while True:
        # Tampilkan menu setiap putaran loop
        display_menu()
        
        try:
            # 2. Minta input dari pengguna (menggunakan .strip() untuk input kosong)
            choice = input(" Masukkan NOMOR produk (1-5) atau 'q' untuk keluar: ").strip()
            
            # PENANGANAN INPUT KOSONG
            if not choice:
                print("\n Input kosong. Silakan masukkan nomor atau 'q'.")
                continue # Kembali ke awal loop
                
            if choice.lower() == 'q':
                print("\nTerima kasih telah menggunakan sistem rekomendasi. Sampai jumpa!")
                break
            
            # Mencoba mengonversi input ke integer
            choice_index = int(choice) - 1
            
            # 3. Validasi pilihan
            if 0 <= choice_index < len(product_list):
                selected_product = product_list[choice_index]
                
                # 4. Panggil fungsi rekomendasi
                recommendations = get_recommendations(selected_product, cosine_sim_matrix, data_frame)
                
                print("\n" + "#"*60)
                print(f"HASIL REKOMENDASI UNTUK: '{selected_product}'")
                print("#"*60)
                
                # Tampilkan hasil dalam format yang rapi
                for i, rec_name in enumerate(recommendations, 1):
                    print(f"Top {i}: {rec_name}")
                print("\n" + "-" * 60)
                
                # Jeda Interaktif: Memaksa pengguna menekan ENTER untuk melanjutkan
                input("Tekan ENTER untuk kembali ke menu pilihan...")
                
            else:
                print("\n❌ Pilihan tidak valid. Silakan masukkan nomor (1-5) yang benar.")
                
        except ValueError:
            # Menangkap error jika input bukan angka dan bukan 'q'
            print("\n❌ Input tidak valid. Mohon masukkan angka (1-5) atau 'q'.")
        except Exception as e:
            print(f"\n❌ Terjadi kesalahan tak terduga: {e}")
            break

# --- JALANKAN PROGRAM INTERAKTIF BARU ---
interactive_recommendation_selector_v2(df, cosine_sim)