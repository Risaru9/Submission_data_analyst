# E-Commerce Analytics Dashboard

## Deskripsi Proyek
Proyek ini bertujuan untuk melakukan analisis data pada **E-Commerce Public Dataset**
guna memahami performa bisnis, perilaku pelanggan, serta distribusi geografis
pelanggan. Hasil analisis disajikan dalam bentuk **dashboard interaktif**
menggunakan **Streamlit** sebagai media visualisasi.

Proyek ini dikembangkan sebagai bagian dari submission analisis data dan
menerapkan proses analisis end-to-end mulai dari pengolahan data hingga
penyajian insight bisnis.

---

## Dataset
Dataset yang digunakan merupakan **E-Commerce Public Dataset** yang terdiri dari
beberapa tabel utama, antara lain:
- `orders`
- `order_items`
- `customers`
- `products`
- `product_category_name_translation`
- `geolocation`

Tidak seluruh tabel dalam dataset digunakan. Pemilihan tabel dilakukan
berdasarkan **relevansi terhadap tujuan analisis dan pertanyaan bisnis**
yang ingin dijawab.

---

## Tahapan Analisis
Tahapan analisis data yang dilakukan dalam proyek ini meliputi:

1. **Data Gathering**  
   Mengumpulkan dan memahami struktur dataset yang digunakan.

2. **Data Cleaning & Preprocessing**  
   Menangani missing values, duplikasi data, serta transformasi data yang
   diperlukan untuk analisis lanjutan.

3. **Exploratory Data Analysis (EDA)**  
   Mengeksplorasi pola data untuk memahami performa penjualan dan distribusi
   kategori produk.

4. **RFM Analysis**  
   Mengelompokkan pelanggan berdasarkan:
   - Recency
   - Frequency
   - Monetary

5. **Geospatial Analysis**  
   Menganalisis distribusi geografis pelanggan berdasarkan lokasi wilayah.

6. **Customer Clustering (Non-Machine Learning)**  
   Segmentasi pelanggan menggunakan pendekatan manual grouping dan binning
   berdasarkan nilai transaksi.

7. **Insight & Business Implication**  
   Menyimpulkan hasil analisis dan implikasinya terhadap strategi bisnis.

---

## Dashboard
Dashboard dikembangkan menggunakan **Streamlit** dan menampilkan beberapa
komponen utama:

- **Business Performance Overview**  
  Ringkasan performa bisnis seperti total revenue, total orders, dan average
  order value.

- **Customer Intelligence**  
  Visualisasi segmentasi pelanggan berdasarkan RFM Analysis dan clustering
  nilai pelanggan.

- **Geographic Distribution**  
  Visualisasi distribusi pelanggan berdasarkan wilayah geografis untuk
  mendukung analisis pasar regional.

Dashboard dirancang agar mudah dipahami dan mampu menyampaikan insight
utama kepada stakeholder non-teknis.

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