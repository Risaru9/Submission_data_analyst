import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling & Color Palette
THEME_COLOR = "#3182ce"
PLOT_TEMPLATE = "plotly_white"

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stMetric {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# Helper Functions untuk Data Processing
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name_english").price.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_rfm_df(df):
    # RFM sederhana on-the-fly untuk data yang difilter
    rfm = df.groupby("customer_id").agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "price": "sum"
    }).reset_index()
    
    rfm.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    # Menghitung Recency
    max_date = df["order_purchase_timestamp"].max()
    rfm["recency"] = rfm["max_order_timestamp"].apply(lambda x: (max_date - x).days)
    
    return rfm

# Load Data
@st.cache_data
def load_data():
    # Load data gabungan (all_data.csv)
    all_df = pd.read_csv("data/all_data.csv")
    
    # Konversi kolom tanggal ke datetime
    datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
    for column in datetime_columns:
        if column in all_df.columns:
            all_df[column] = pd.to_datetime(all_df[column])
            
    return all_df

all_df = load_data()

# ------------------------------------------------------------------------
# SIDEBAR (FITUR INTERAKTIF - KRITERIA WAJIB)
# ------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=50)
    st.title("Filter Data")
    
    # Filter Rentang Waktu
    min_date = all_df["order_purchase_timestamp"].min()
    max_date = all_df["order_purchase_timestamp"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Dataframe Utama berdasarkan Input Sidebar
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

# Menyiapkan Dataframe Turunan dari Data yang Sudah Difilter
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
rfm_df = create_rfm_df(main_df)

# ------------------------------------------------------------------------
# MAIN DASHBOARD
# ------------------------------------------------------------------------
st.header("E-Commerce Dashboard :sparkles:")
st.markdown("Dashboard ini menampilkan performa penjualan berdasarkan rentang waktu yang dipilih.")

# 1. Business Overview (Metric Cards)
st.subheader("Daily Orders & Revenue")

col1, col2, col3 = st.columns(3)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)

with col2:
    total_revenue = daily_orders_df.revenue.sum()
    st.metric("Total Revenue", value=f"R$ {total_revenue:,.0f}")

with col3:
    # Average Order Value (Revenue / Orders)
    if total_orders > 0:
        aov = total_revenue / total_orders
    else:
        aov = 0
    st.metric("Average Order Value", value=f"R$ {aov:,.2f}")

# Grafik Tren Harian (Line Chart)
fig_daily = px.line(
    daily_orders_df, 
    x="order_purchase_timestamp", 
    y="revenue", 
    title="Tren Pendapatan Harian",
    template=PLOT_TEMPLATE
)
fig_daily.update_traces(line_color=THEME_COLOR)
st.plotly_chart(fig_daily, use_container_width=True)

# 2. Product Performance
st.subheader("Best Performing Product Categories")

col_chart, col_insight = st.columns([2, 1])

with col_chart:
    top_5_cat = sum_order_items_df.head(5)
    
    fig_cat = px.bar(
        top_5_cat,
        x="price",
        y="product_category_name_english",
        orientation="h",
        title="Top 5 Kategori Produk (Revenue)",
        labels={"price": "Revenue", "product_category_name_english": "Category"},
        template=PLOT_TEMPLATE
    )
    fig_cat.update_traces(marker_color=THEME_COLOR)
    st.plotly_chart(fig_cat, use_container_width=True)

with col_insight:
    st.markdown("##### Insight")
    if not top_5_cat.empty:
        best_cat = top_5_cat.iloc[0]['product_category_name_english']
        st.info(f"""
        Berdasarkan filter tanggal yang Anda pilih, kategori **{best_cat}** memiliki performa penjualan terbaik.
        """)
    else:
        st.warning("Tidak ada data pada rentang tanggal ini.")

# 3. Customer Demographics (RFM & Geo)
st.subheader("Customer Intelligence")
tab1, tab2 = st.tabs(["RFM Analysis", "Geographic Distribution"])

with tab1:
    col_rfm1, col_rfm2 = st.columns(2)
    
    with col_rfm1:
        st.markdown("**Distribusi Recency**")
        fig_recency = px.histogram(
            rfm_df, 
            x="recency", 
            nbins=30, 
            title="Seberapa baru pelanggan bertransaksi?",
            template=PLOT_TEMPLATE
        )
        fig_recency.update_traces(marker_color=THEME_COLOR)
        st.plotly_chart(fig_recency, use_container_width=True)
        
    with col_rfm2:
        st.markdown("**Distribusi Monetary**")
        fig_monetary = px.histogram(
            rfm_df, 
            x="monetary", 
            nbins=30, 
            title="Sebaran Nilai Belanja Pelanggan",
            template=PLOT_TEMPLATE
        )
        fig_monetary.update_traces(marker_color=THEME_COLOR)
        st.plotly_chart(fig_monetary, use_container_width=True)

with tab2:
    st.markdown("**Sebaran Lokasi Pelanggan (Top 10 States)**")
    
    # Menghitung geo berdasarkan data yang difilter
    by_state = main_df.groupby("customer_state").customer_id.nunique().reset_index()
    by_state.rename(columns={"customer_id": "customer_count"}, inplace=True)
    top_states = by_state.sort_values(by="customer_count", ascending=False).head(10)
    
    fig_geo = px.bar(
        top_states,
        x="customer_count",
        y="customer_state",
        orientation="h",
        title="Jumlah Pelanggan per Negara Bagian",
        template=PLOT_TEMPLATE
    )
    fig_geo.update_traces(marker_color=THEME_COLOR)
    st.plotly_chart(fig_geo, use_container_width=True)

# Footer
st.caption("Copyright © Dicoding 2024")