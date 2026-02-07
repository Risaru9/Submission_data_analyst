import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    layout="wide"
)

# COLOR
COLOR_PRIMARY = "#3B82F6"
COLOR_SUCCESS = "#22C55E"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER  = "#EF4444"
COLOR_NEUTRAL = "#94A3B8"

# LOAD DATA
kpi = pd.read_csv("data/dashboard_kpi_summary.csv")
revenue_cat = pd.read_csv("data/dashboard_revenue_by_category.csv")
rfm_segment = pd.read_csv("data/dashboard_rfm_segment_summary.csv")
monetary_cluster = pd.read_csv("data/dashboard_monetary_cluster_summary.csv")
customers = pd.read_csv("data/customers_dataset.csv")

# HEADER
st.title("E-Commerce Analytics Dashboard")
st.caption(
    "Analytical dashboard based on E-Commerce Public Dataset. "
    "This dashboard summarizes business performance, customer behavior, "
    "and geographic distribution of customers."
)

st.markdown("---")

# TABS
tab1, tab2, tab3 = st.tabs([
    "Business Performance",
    "Customer Intelligence",
    "Geographic Distribution"
])

# TAB 1 — BUSINESS PERFORMANCE
with tab1:

    st.subheader("Business Performance Overview")

    # KPI SECTION
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Revenue", f"{kpi.total_revenue[0]:,.0f}")
    col2.metric("Total Orders", f"{kpi.total_orders[0]:,}")
    col3.metric("Total Customers", f"{kpi.total_customers[0]:,}")
    col4.metric("Average Order Value", f"{kpi.avg_order_value[0]:,.0f}")
    col5.metric("Average Customer Value", f"{kpi.avg_customer_value[0]:,.0f}")

    st.markdown("---")

    # REVENUE BY CATEGORY
    left, right = st.columns([2, 1])

    with left:
        fig_rev = px.bar(
            revenue_cat.head(10),
            x="price",
            y="product_category_name_english",
            orientation="h",
            title="Top Product Categories by Revenue",
            labels={
                "price": "Total Revenue",
                "product_category_name_english": "Product Category"
            },
            color_discrete_sequence=[COLOR_PRIMARY]
        )
        fig_rev.update_layout(height=420)
        st.plotly_chart(fig_rev, use_container_width=True)

    with right:
        st.subheader("Key Insight")
        st.write(
            "Revenue terkonsentrasi pada sejumlah kecil kategori produk utama. "
            "Kategori-kategori ini menjadi penggerak utama pendapatan dan "
            "memiliki potensi terbesar untuk dioptimalkan melalui strategi "
            "promosi dan ketersediaan produk."
        )

# TAB 2 — CUSTOMER INTELLIGENCE
with tab2:

    st.subheader("Customer Intelligence Overview")

    # RFM SEGMENT
    col1, col2 = st.columns([2, 1])

    with col1:
        fig_rfm = px.bar(
            rfm_segment,
            x="total_customers",
            y="segment",
            orientation="h",
            title="Customer Distribution by RFM Segment",
            labels={
                "total_customers": "Number of Customers",
                "segment": "Customer Segment"
            },
            color_discrete_sequence=[COLOR_SUCCESS]
        )
        fig_rfm.update_layout(height=420)
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col2:
        st.subheader("RFM Insight")
        st.write(
            "Sebagian besar pelanggan berada pada segmen menengah seperti "
            "Potential dan Loyal Customer. Segmen Champion jumlahnya lebih kecil "
            "namun memiliki nilai strategis tinggi terhadap pendapatan."
        )

    st.markdown("---")

    # MONETARY CLUSTER
    col1, col2 = st.columns([2, 1])

    with col1:
        fig_cluster = px.bar(
            monetary_cluster,
            x="total_customers",
            y="monetary_cluster",
            orientation="h",
            title="Customer Clustering Based on Monetary Value",
            labels={
                "total_customers": "Number of Customers",
                "monetary_cluster": "Customer Cluster"
            },
            color_discrete_sequence=[COLOR_WARNING]
        )
        fig_cluster.update_layout(height=420)
        st.plotly_chart(fig_cluster, use_container_width=True)

    with col2:
        st.subheader("Clustering Insight")
        st.write(
            "Kelompok pelanggan bernilai tinggi dan sangat tinggi memiliki jumlah "
            "yang relatif kecil, namun kontribusinya signifikan terhadap total "
            "pendapatan. Fokus retensi dan personalisasi sebaiknya diarahkan "
            "pada kelompok ini."
        )

# TAB 3 — GEOGRAPHIC DISTRIBUTION
with tab3:

    st.subheader("Geographic Distribution of Customers")

    # AGGREGATE CUSTOMER BY STATE
    geo_df = (
        customers
        .groupby("customer_state")
        .size()
        .reset_index(name="total_customers")
        .sort_values("total_customers", ascending=False)
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        fig_geo = px.bar(
            geo_df.head(10),
            x="total_customers",
            y="customer_state",
            orientation="h",
            title="Top Regions by Number of Customers",
            labels={
                "total_customers": "Number of Customers",
                "customer_state": "State"
            },
            color_discrete_sequence=[COLOR_PRIMARY]
        )
        fig_geo.update_layout(height=420)
        st.plotly_chart(fig_geo, use_container_width=True)

    with col2:
        st.subheader("Geographic Insight")
        st.write(
            "Distribusi pelanggan menunjukkan konsentrasi yang lebih tinggi pada "
            "wilayah tertentu. Informasi ini dapat dimanfaatkan untuk strategi "
            "pemasaran regional, optimasi logistik, dan perencanaan ekspansi pasar."
        )

st.markdown("---")
st.caption("E-Commerce Public Dataset | Analytical Dashboard")
