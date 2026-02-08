import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling & Color Palette
# Menggunakan palet biru yang selaras untuk tampilan profesional
THEME_COLOR = "#3182ce"  # Primary Blue
PLOT_TEMPLATE = "plotly_white"  # Bersih, background putih

st.markdown("""
    <style>
        /* Mengatur padding atas agar tidak terlalu renggang */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Styling kartu metrik agar lebih modern */
        .stMetric {
            background-color: #000;
            border: 1px solid #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# Data Loading
@st.cache_data
def load_data():
    try:
        # Load data utama
        kpi = pd.read_csv("data/kpi_summary.csv")
        rev_cat = pd.read_csv("data/revenue_by_category.csv")
        rfm = pd.read_csv("data/rfm_score.csv")
        cust_seg = pd.read_csv("data/customer_segment.csv")
        geo = pd.read_csv("data/geo_summary.csv")
        seller = pd.read_csv("data/seller_performance.csv")
        payment = pd.read_csv("data/payment_summary.csv")
        
        try:
            reviews = pd.read_csv("data/review_summary.csv")
        except FileNotFoundError:
            reviews = pd.DataFrame({'review_score': [1,2,3,4,5], 'avg_price': [0,0,0,0,0]})
            
        return kpi, rev_cat, rfm, cust_seg, geo, seller, payment, reviews
    except FileNotFoundError as e:
        st.error(f"Data tidak ditemukan: {e}. Pastikan file CSV ada di folder 'data/'.")
        return None, None, None, None, None, None, None, None

# Inisialisasi Data
kpi_df, rev_cat_df, rfm_df, cust_seg_df, geo_df, seller_df, payment_df, review_df = load_data()

if kpi_df is None:
    st.stop()

# Sidebar
with st.sidebar:
    st.title("E-Commerce Analyst")
    st.markdown("**Menu Navigasi**")
    st.info("Dashboard ini menampilkan hasil analisis performa bisnis, pelanggan, dan operasional.")

# Main Header
st.title("E-Commerce Analytics Dashboard")
st.markdown("Ringkasan performa bisnis dan analisis perilaku pelanggan.")
st.markdown("---")

# 1. Business Overview
st.subheader("Business Performance")

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"R$ {kpi_df['total_revenue'][0]:,.0f}")
col2.metric("Total Orders", f"{kpi_df['total_orders'][0]:,}")
col3.metric("Total Customers", f"{kpi_df['total_customers'][0]:,}")
col4.metric("Avg. Order Value", f"R$ {kpi_df['average_order_value'][0]:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# Revenue Chart & Insight
col_chart, col_insight = st.columns([2, 1])

with col_chart:
    top_cat = rev_cat_df.head(10).sort_values("price", ascending=True)
    
    fig_rev = px.bar(
        top_cat,
        x="price",
        y="product_category_name_english",
        orientation="h",
        title="Top 10 Product Categories by Revenue",
        labels={"price": "Revenue (R$)", "product_category_name_english": "Category"},
        template=PLOT_TEMPLATE
    )
    # Menyelaraskan warna bar dengan tema
    fig_rev.update_traces(marker_color=THEME_COLOR)
    st.plotly_chart(fig_rev, use_container_width=True)

with col_insight:
    st.markdown("##### Key Insight")
    best_cat = top_cat.iloc[-1]['product_category_name_english']
    st.success(f"""
    **Kategori Unggulan:**
    
    Kategori **{best_cat}** menjadi penyumbang pendapatan terbesar.
    
    Disarankan untuk memprioritaskan stok dan budget marketing pada kategori ini untuk memaksimalkan profitabilitas.
    """)

st.markdown("---")

# 2. Detailed Analysis Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Customer Intelligence",
    "Payment & Reviews",
    "Geography",
    "Seller Performance"
])

# Tab 1: Customer Intelligence
with tab1:
    st.subheader("Analisis Pelanggan (RFM & Segmentasi)")
    
    col_rfm, col_seg = st.columns(2)
    
    with col_rfm:
        # Boxplot RFM
        fig_recency = px.box(
            rfm_df, 
            y="recency", 
            title="Distribusi Recency (Hari sejak pembelian terakhir)",
            template=PLOT_TEMPLATE
        )
        fig_recency.update_traces(marker_color=THEME_COLOR)
        st.plotly_chart(fig_recency, use_container_width=True)
        
    with col_seg:
        # Bar Chart Segmentasi
        seg_counts = cust_seg_df['monetary_segment'].value_counts().reset_index()
        seg_counts.columns = ['segment', 'count']
        
        fig_seg = px.bar(
            seg_counts,
            x='segment',
            y='count',
            title="Jumlah Pelanggan per Segmen Nilai",
            text='count',
            template=PLOT_TEMPLATE
        )
        fig_seg.update_traces(marker_color=THEME_COLOR)
        st.plotly_chart(fig_seg, use_container_width=True)

# Tab 2: Payment & Satisfaction
with tab2:
    col_pay, col_rev = st.columns(2)
    
    with col_pay:
        st.subheader("Metode Pembayaran")
        # Mencari kolom value secara dinamis
        val_col = [c for c in payment_df.columns if 'val' in c or 'price' in c or 'sum' in c][0]
        
        fig_pay = px.pie(
            payment_df,
            values=val_col,
            names=payment_df.columns[0],
            title="Proporsi Tipe Pembayaran",
            hole=0.4,
            template=PLOT_TEMPLATE,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        st.plotly_chart(fig_pay, use_container_width=True)

    with col_rev:
        st.subheader("Hubungan Rating & Harga")
        fig_sat = px.bar(
            review_df,
            x="review_score",
            y="avg_price",
            title="Rata-rata Transaksi berdasarkan Rating",
            labels={"avg_price": "Avg Value", "review_score": "Rating"},
            template=PLOT_TEMPLATE
        )
        fig_sat.update_traces(marker_color=THEME_COLOR)
        st.plotly_chart(fig_sat, use_container_width=True)

# Tab 3: Geography
with tab3:
    st.subheader("Sebaran Lokasi Pelanggan")
    
    col_geo, col_desc = st.columns([2, 1])
    
    with col_geo:
        geo_x = geo_df.columns[0]
        geo_y = geo_df.columns[1]
        top_geo = geo_df.sort_values(geo_y, ascending=False).head(10)
        
        fig_geo = px.bar(
            top_geo,
            x=geo_y,
            y=geo_x,
            orientation='h',
            title="Top 10 Wilayah Pelanggan",
            template=PLOT_TEMPLATE
        )
        fig_geo.update_traces(marker_color=THEME_COLOR)
        st.plotly_chart(fig_geo, use_container_width=True)
        
    with col_desc:
        st.info("Wilayah teratas menunjukkan area dengan densitas pelanggan tertinggi, cocok untuk fokus ekspansi logistik.")

# Tab 4: Seller Performance
with tab4:
    st.subheader("Performa Penjual")
    
    # Deteksi kolom numerik
    num_cols = seller_df.select_dtypes(include=['number']).columns
    col_ord = num_cols[0]
    col_rev = num_cols[1] if len(num_cols) > 1 else num_cols[0]
    
    fig_seller = px.scatter(
        seller_df,
        x=col_ord,
        y=col_rev,
        title="Sebaran Performa Seller (Order vs Revenue)",
        labels={col_ord: "Total Orders", col_rev: "Total Revenue"},
        opacity=0.6,
        template=PLOT_TEMPLATE
    )
    fig_seller.update_traces(marker_color=THEME_COLOR)
    st.plotly_chart(fig_seller, use_container_width=True)

# Footer
st.markdown("---")
st.caption("© 2024 E-Commerce Analytics Project")