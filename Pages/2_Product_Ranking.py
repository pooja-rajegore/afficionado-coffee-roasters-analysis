import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# -------------------------
# Load Data
# -------------------------

df = load_data()

# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["product_category"].unique())
)

product_type = st.sidebar.multiselect(
    "Product Type",
    sorted(df["product_type"].unique())
)

location = st.sidebar.multiselect(
    "Store Location",
    sorted(df["store_location"].unique())
)

top_n = st.sidebar.slider(
    "Top N Products",
    min_value=5,
    max_value=30,
    value=10
)

# -------------------------
# Apply Filters
# -------------------------

filtered_df = df.copy()

if category:
    filtered_df = filtered_df[
        filtered_df["product_category"].isin(category)
    ]

if product_type:
    filtered_df = filtered_df[
        filtered_df["product_type"].isin(product_type)
    ]

if location:
    filtered_df = filtered_df[
        filtered_df["store_location"].isin(location)
    ]

# -------------------------
# Page Title
# -------------------------

st.title("🏆 Product Ranking Analysis")

st.markdown(
    "Compare products by **Revenue** and **Sales Volume**."
)

st.markdown("---")

# -------------------------
# Top Revenue Products
# -------------------------

revenue_rank = (
    filtered_df
    .groupby("product_detail")["revenue"]
    .sum()
    .reset_index()
    .sort_values(
        by="revenue",
        ascending=False
    )
    .head(top_n)
)

st.subheader("💰 Top Products by Revenue")

fig1 = px.bar(
    revenue_rank,
    x="revenue",
    y="product_detail",
    orientation="h",
    text_auto=".2s",
    title=f"Top {top_n} Products by Revenue"
)

fig1.update_layout(
    height=500,
    yaxis_title="Product",
    xaxis_title="Revenue"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -------------------------
# Top Volume Products
# -------------------------

volume_rank = (
    filtered_df
    .groupby("product_detail")["transaction_qty"]
    .sum()
    .reset_index()
    .sort_values(
        by="transaction_qty",
        ascending=False
    )
    .head(top_n)
)

st.subheader("📦 Top Products by Sales Volume")

fig2 = px.bar(
    volume_rank,
    x="transaction_qty",
    y="product_detail",
    orientation="h",
    text_auto=True,
    title=f"Top {top_n} Products by Units Sold"
)

fig2.update_layout(
    height=500,
    yaxis_title="Product",
    xaxis_title="Units Sold"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -------------------------
# Revenue vs Volume Ranking
# -------------------------

st.subheader("📊 Revenue vs Volume Comparison")

comparison = (
    filtered_df
    .groupby("product_detail")
    .agg({
        "transaction_qty": "sum",
        "revenue": "sum"
    })
    .reset_index()
    .sort_values(
        by="revenue",
        ascending=False
    )
)

st.dataframe(
    comparison,
    use_container_width=True
)

# -------------------------
# Download Option
# -------------------------

csv = comparison.to_csv(index=False)

st.download_button(
    label="⬇ Download Ranking Report",
    data=csv,
    file_name="product_ranking.csv",
    mime="text/csv"
)
