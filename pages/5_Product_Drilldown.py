import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# -------------------------
# Load Data
# -------------------------

df = load_data()

# -------------------------
# Page Title
# -------------------------

st.title("🔍 Product Drill-Down Analysis")

st.markdown("""
Analyze the detailed performance of individual products.
""")

st.markdown("---")

# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("Filters")

selected_product = st.sidebar.selectbox(
    "Select Product",
    sorted(df["product_detail"].unique())
)

# -------------------------
# Filter Data
# -------------------------

product_df = df[
    df["product_detail"] == selected_product
]

# -------------------------
# KPI Calculations
# -------------------------

total_revenue = product_df["revenue"].sum()

total_units = product_df["transaction_qty"].sum()

avg_price = product_df["unit_price"].mean()

transactions = len(product_df)

# -------------------------
# KPI Cards
# -------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue",
    f"{total_revenue:,.2f}"
)

col2.metric(
    "Units Sold",
    f"{total_units:,}"
)

col3.metric(
    "Average Price",
    f"{avg_price:.2f}"
)

col4.metric(
    "Transactions",
    transactions
)

st.markdown("---")

# -------------------------
# Product Information
# -------------------------

st.subheader("📋 Product Details")

info = product_df[
    [
        "product_category",
        "product_type",
        "product_detail"
    ]
].drop_duplicates()

st.dataframe(
    info,
    use_container_width=True
)

# -------------------------
# Store Performance
# -------------------------

st.subheader("🏪 Store-wise Performance")

store_perf = (
    product_df
    .groupby("store_location")
    .agg(
        Revenue=("revenue", "sum"),
        Units_Sold=("transaction_qty", "sum")
    )
    .reset_index()
)

fig1 = px.bar(
    store_perf,
    x="store_location",
    y="Revenue",
    text_auto=".2s",
    title="Revenue by Store"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -------------------------
# Revenue vs Units
# -------------------------

fig2 = px.bar(
    store_perf,
    x="store_location",
    y="Units_Sold",
    text_auto=True,
    title="Units Sold by Store"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -------------------------
# Store Summary Table
# -------------------------

st.subheader("📊 Store Performance Table")

st.dataframe(
    store_perf,
    use_container_width=True
)

# -------------------------
# Transaction Details
# -------------------------

st.subheader("🧾 Transaction Details")

st.dataframe(
    product_df,
    use_container_width=True
)

# -------------------------
# Revenue Contribution
# -------------------------

st.subheader("💰 Revenue Contribution")

total_company_revenue = df["revenue"].sum()

contribution = (
    total_revenue /
    total_company_revenue
) * 100

st.metric(
    "Revenue Contribution %",
    f"{contribution:.2f}%"
)

# -------------------------
# Download Report
# -------------------------

csv = product_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Product Report",
    data=csv,
    file_name=f"{selected_product}_report.csv",
    mime="text/csv"
)
