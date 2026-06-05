import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# ----------------------------------
# Page Config
# ----------------------------------

st.set_page_config(
    page_title="Afficionado Coffee Analytics",
    page_icon="☕",
    layout="wide"
)

# ----------------------------------
# Load Data
# ----------------------------------

df = load_data()

# ----------------------------------
# Custom CSS
# ----------------------------------

st.markdown("""
<style>

[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e6e6e6;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# Sidebar Filters
# ----------------------------------

st.sidebar.title("☕ Dashboard Filters")

category = st.sidebar.multiselect(
    "Product Category",
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

# ----------------------------------
# Apply Filters
# ----------------------------------

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

# ----------------------------------
# KPIs
# ----------------------------------

total_revenue = filtered_df["revenue"].sum()

total_units = filtered_df["transaction_qty"].sum()

total_products = filtered_df["product_detail"].nunique()

total_categories = filtered_df["product_category"].nunique()

avg_revenue = filtered_df["revenue"].mean()

# ----------------------------------
# Header
# ----------------------------------

st.title("☕ Afficionado Coffee Roasters")

st.subheader(
    "Product Optimization & Revenue Contribution Analysis"
)

st.markdown("---")

# ----------------------------------
# KPI Cards
# ----------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}"
)

col2.metric(
    "Units Sold",
    f"{total_units:,}"
)

col3.metric(
    "Products",
    total_products
)

col4.metric(
    "Categories",
    total_categories
)

col5.metric(
    "Avg Revenue",
    f"{avg_revenue:,.2f}"
)

st.markdown("---")

# ----------------------------------
# Top Products Section
# ----------------------------------

st.subheader(f"🏆 Top {top_n} Products by Revenue")

top_products = (
    filtered_df
    .groupby("product_detail")
    .agg(
        Revenue=("revenue", "sum"),
        Units_Sold=("transaction_qty", "sum")
    )
    .reset_index()
    .sort_values(
        by="Revenue",
        ascending=False
    )
    .head(top_n)
)

st.dataframe(
    top_products,
    use_container_width=True
)

# ----------------------------------
# Revenue Chart
# ----------------------------------

fig = px.bar(
    top_products,
    x="Revenue",
    y="product_detail",
    orientation="h",
    text_auto=".2s",
    title=f"Top {top_n} Products by Revenue"
)

fig.update_layout(
    height=600,
    yaxis_title="Product",
    xaxis_title="Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Revenue by Category
# ----------------------------------

st.subheader("📊 Revenue Distribution by Category")

category_rev = (
    filtered_df
    .groupby("product_category")["revenue"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    category_rev,
    names="product_category",
    values="revenue",
    hole=0.6
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ----------------------------------
# Data Preview
# ----------------------------------

st.subheader("📋 Filtered Data Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ----------------------------------
# Footer
# ----------------------------------

st.markdown("---")

st.caption(
    "Afficionado Coffee Roasters | Streamlit Analytics Dashboard"
)
