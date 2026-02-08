cat << 'EOF' > README.md
# E-Commerce Analytics Dashboard

## Deskripsi Proyek
Proyek ini bertujuan untuk melakukan analisis data pada **E-Commerce Public Dataset**
guna memahami performa bisnis, perilaku pelanggan, preferensi pembayaran,
kualitas layanan, serta distribusi geografis pelanggan.
Hasil analisis disajikan dalam bentuk **dashboard interaktif menggunakan Streamlit**
sebagai media visualisasi dan penyampaian insight bisnis.

Proyek ini dikembangkan sebagai bagian dari submission analisis data dan
menerapkan proses analisis **end-to-end**, mulai dari pengolahan data mentah,
analisis eksploratif, analisis lanjutan, hingga penyajian hasil dalam dashboard.

---

## Dataset
Dataset yang digunakan merupakan **E-Commerce Public Dataset** yang terdiri dari
beberapa tabel utama, antara lain:

- orders  
- order_items  
- order_payments  
- order_reviews  
- customers  
- products  
- product_category_name_translation  
- geolocation  
- sellers  

Tidak seluruh tabel mentah digunakan secara langsung pada dashboard.
Pemilihan tabel dan kolom dilakukan berdasarkan **relevansi terhadap tujuan analisis
dan pertanyaan bisnis** yang ingin dijawab.

---

## Tahapan Analisis
Tahapan analisis data yang dilakukan dalam proyek ini meliputi:

1. **Data Gathering**  
   Mengumpulkan dan memahami struktur serta relasi antar dataset.

2. **Data Cleaning & Preprocessing**  
   Menangani missing values, duplikasi data, standarisasi data, serta
   penggabungan dataset yang diperlukan untuk analisis lanjutan.

3. **Exploratory Data Analysis (EDA)**  
   Mengeksplorasi pola data untuk memahami performa penjualan,
   distribusi kategori produk, dan karakteristik transaksi.

4. **RFM Analysis**  
   Menganalisis perilaku pelanggan berdasarkan:
   - Recency  
   - Frequency  
   - Monetary  

5. **Customer Clustering (Non-Machine Learning)**  
   Segmentasi pelanggan menggunakan pendekatan rule-based dan binning
   berdasarkan nilai transaksi.

6. **Payment & Customer Satisfaction Analysis**  
   Analisis metode pembayaran serta hubungan antara rating ulasan pelanggan
   dengan nilai transaksi.

7. **Geospatial Analysis**  
   Analisis distribusi geografis pelanggan untuk mengidentifikasi wilayah
   dengan konsentrasi pelanggan tertinggi dan potensi pasar regional.

8. **Seller Performance Analysis**  
   Analisis performa seller berdasarkan jumlah pesanan dan pendapatan.

9. **Insight & Business Recommendation**  
   Penyusunan kesimpulan dan rekomendasi bisnis berbasis data.

---

## Data untuk Dashboard
Dashboard Streamlit **tidak menggunakan data mentah secara langsung**.
Sebagai gantinya, dashboard memanfaatkan **data hasil analisis yang telah
diagregasi dan disimpan dalam bentuk file CSV**.

Pendekatan ini dilakukan untuk:
- meningkatkan performa dashboard,
- menjaga pemisahan antara proses analisis dan visualisasi,
- menerapkan praktik kerja analisis data yang profesional.

---

## Dashboard
Dashboard dikembangkan menggunakan **Streamlit** dan **Plotly** dengan tampilan
interaktif dan terstruktur. Dashboard menampilkan beberapa komponen utama berikut:

### Business Performance Overview
- Total Revenue  
- Total Orders  
- Total Customers  
- Average Order Value  
- Top kategori produk berdasarkan kontribusi pendapatan  

### Customer Intelligence
- Distribusi Recency pelanggan  
- Segmentasi pelanggan berdasarkan nilai transaksi  
- Insight perilaku pelanggan berdasarkan RFM Analysis  

### Payment & Customer Satisfaction
- Distribusi metode pembayaran  
- Hubungan antara rating ulasan dan nilai transaksi  

### Geographic Distribution
- Top wilayah dengan jumlah pelanggan terbanyak  
- Insight potensi pasar regional  

### Seller Performance
- Performa seller berdasarkan jumlah pesanan dan pendapatan  

Dashboard dirancang agar mudah dipahami oleh stakeholder non-teknis dan
mampu menyampaikan insight bisnis secara jelas.

---

## Cara Menjalankan Dashboard

### 1. Install Dependencies
Pastikan Python telah terpasang, kemudian install seluruh dependency:

```bash
pip install -r requirements.txt
```
### 2. Jalankan Aplikasi Streamlit

Jalankan dashboard dengan perintah berikut:
```bash
streamlit run dashboard/dashboard.py
```
Dashboard akan terbuka secara otomatis melalui browser.