import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLORS = {
    "primary": "#6366F1",
    "secondary": "#10B981",
    "accent": "#F59E0B",
    "danger": "#EF4444",
    "bg_dark": "#0E1117",
    "card_bg": "#1E1E1E",
    "text": "#FAFAFA"
}

st.markdown(f"""
<style>
    .stApp {{
        background-color: {COLORS['bg_dark']};
        color: {COLORS['text']};
    }}
    [data-testid="stSidebar"] {{
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }}
    div[data-testid="metric-container"] {{
        background-color: {COLORS['card_bg']};
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }}
    div[data-testid="metric-container"]:hover {{
        border-color: {COLORS['primary']};
    }}
    div[data-testid="metric-container"] label {{ color: #9CA3AF; }}
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {{ color: #F3F4F6; }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    div[data-testid="stDateInput"] div, div[data-testid="stSelectbox"] div {{
        color: #FFFFFF;
    }}
    .stDataFrame {{
        border: 1px solid #30363D;
        border-radius: 5px;
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/all_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("File data/all_data.csv tidak ditemukan.")
    st.stop()

with st.sidebar:
    st.header("Filter Dashboard")
    
    min_date = df["order_purchase_timestamp"].min()
    max_date = df["order_purchase_timestamp"].max()

    date_range = st.date_input(
        "Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    unique_cats = sorted(df["product_category_name_english"].dropna().unique())
    category = st.selectbox("Kategori Produk", ["All"] + unique_cats)

    unique_states = sorted(df["customer_state"].dropna().unique())
    state = st.selectbox("Wilayah Pelanggan", ["All"] + unique_states)
    
    st.markdown("---")
    st.write("Export Data")
    
    if isinstance(date_range, list) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered = df[
            (df["order_purchase_timestamp"].dt.date >= start_date) &
            (df["order_purchase_timestamp"].dt.date <= end_date)
        ]
    else:
        filtered = df

    if category != "All":
        filtered = filtered[filtered["product_category_name_english"] == category]

    if state != "All":
        filtered = filtered[filtered["customer_state"] == state]

    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

if filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini.")
    st.stop()

rfm_df = filtered.groupby("customer_id").agg({
    "order_purchase_timestamp": "max",
    "order_id": "nunique",
    "price": "sum"
}).reset_index()

rfm_df.columns = ["customer_id", "max_date", "frequency", "monetary"]
max_date_filter = filtered["order_purchase_timestamp"].max()
rfm_df["recency"] = (max_date_filter - rfm_df["max_date"]).dt.days

def segment_customer(row):
    if row["recency"] < 30 and row["monetary"] > 100:
        return "Champions"
    elif row["recency"] < 90:
        return "Active"
    elif row["monetary"] > 1000:
        return "Whales"
    elif row["recency"] > 180:
        return "Hibernating"
    else:
        return "Potential"

rfm_df["segment"] = rfm_df.apply(segment_customer, axis=1)

st.title("E-Commerce Analytics Dashboard")

total_orders = filtered["order_id"].nunique()
total_revenue = filtered["price"].sum()
aov = total_revenue / total_orders if total_orders > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("Total Orders", f"{total_orders:,}")
c2.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
c3.metric("Avg. Order Value", f"R$ {aov:,.2f}")

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview", 
    "RFM Analysis", 
    "Clustering", 
    "Geospatial"
])

with tab1:
    col_trend, col_cat = st.columns([2, 1])
    
    with col_trend:
        st.subheader("Tren Pendapatan")
        daily = filtered.set_index("order_purchase_timestamp").resample("D").price.sum().reset_index()
        
        fig_trend = px.area(
            daily, x="order_purchase_timestamp", y="price",
            template="plotly_dark",
            labels={"order_purchase_timestamp": "Tanggal", "price": "Revenue"}
        )
        fig_trend.update_traces(line_color=COLORS["primary"], fillcolor="rgba(99, 102, 241, 0.2)")
        fig_trend.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_cat:
        st.subheader("Top Kategori")
        top_cat = filtered.groupby("product_category_name_english").price.sum().sort_values(ascending=False).head(5).reset_index()
        
        fig_cat = px.bar(
            top_cat, x="price", y="product_category_name_english", orientation="h",
            template="plotly_dark",
            labels={"price": "Revenue", "product_category_name_english": ""}
        )
        fig_cat.update_traces(marker_color=COLORS["secondary"])
        fig_cat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with st.expander("Lihat Data Transaksi Harian"):
        st.dataframe(daily.sort_values("order_purchase_timestamp", ascending=False), use_container_width=True)

with tab2:
    st.subheader("Analisis RFM")
    
    c_rec, c_mon = st.columns(2)
    with c_rec:
        fig_rec = px.histogram(
            rfm_df, x="recency", nbins=30, 
            title="Distribusi Recency", 
            template="plotly_dark",
            labels={"recency": "Hari sejak pembelian terakhir"}
        )
        fig_rec.update_traces(marker_color=COLORS["accent"])
        fig_rec.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_rec, use_container_width=True)
        
    with c_mon:
        fig_mon = px.histogram(
            rfm_df, x="monetary", nbins=30, 
            title="Distribusi Monetary", 
            template="plotly_dark",
            labels={"monetary": "Total Nilai Transaksi"}
        )
        fig_mon.update_traces(marker_color=COLORS["danger"])
        fig_mon.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_mon, use_container_width=True)
    
    with st.expander("Lihat Data RFM"):
        st.dataframe(rfm_df.head(100), use_container_width=True)

with tab3:
    st.subheader("Analisis Clustering")
    
    seg_counts = rfm_df["segment"].value_counts().reset_index()
    seg_counts.columns = ["segment", "count"]
    
    col_cluster_chart, col_cluster_desc = st.columns([2, 1])
    
    with col_cluster_chart:
        fig_seg = px.bar(
            seg_counts, x="segment", y="count",
            title="Jumlah Pelanggan per Cluster",
            template="plotly_dark",
            color="segment",
            labels={"segment": "Cluster", "count": "Jumlah Pelanggan"}
        )
        fig_seg.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_seg, use_container_width=True)
        
    with col_cluster_desc:
        st.write("Definisi Cluster")
        st.markdown("""
        - **Champions**: Baru saja bertransaksi & nilai transaksi tinggi
        - **Whales**: Total nilai transaksi sangat besar
        - **Active**: Bertransaksi dalam 3 bulan terakhir
        - **Hibernating**: Tidak bertransaksi > 6 bulan
        - **Potential**: Pelanggan lainnya
        """)
    
    with st.expander("Lihat Data Segmentasi"):
        st.dataframe(seg_counts, use_container_width=True)

with tab4:
    st.subheader("Analisis Geospatial")
    
    geo = filtered.groupby("customer_state").customer_id.nunique().reset_index(name="count").sort_values("count", ascending=False)
    
    fig_geo = px.bar(
        geo.head(10), x="count", y="customer_state", orientation="h",
        title="Top 10 Wilayah Pelanggan",
        template="plotly_dark",
        labels={"count": "Jumlah Pelanggan", "customer_state": "Kode Wilayah"}
    )
    fig_geo.update_traces(marker_color=COLORS["primary"])
    fig_geo.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig_geo, use_container_width=True)
    
    with st.expander("Lihat Data Wilayah"):
        st.dataframe(geo, use_container_width=True)