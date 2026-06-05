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

location = st.sidebar.multiselect(
    "Store Location",
    sorted(df["store_location"].unique())
)

if location:
    df = df[
        df["store_location"].isin(location)
    ]

# -------------------------
# Page Title
# -------------------------

st.title("📊 Category Performance Analysis")

st.markdown("""
Analyze revenue distribution across product categories
and product types.
""")

st.markdown("---")

# -------------------------
# KPI Calculations
# -------------------------

total_revenue = df["revenue"].sum()

top_category = (
    df.groupby("product_category")["revenue"]
      .sum()
      .idxmax()
)

top_category_revenue = (
    df.groupby("product_category")["revenue"]
      .sum()
      .max()
)

num_categories = (
    df["product_category"]
      .nunique()
)

# -------------------------
# KPI Cards
# -------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}"
)

col2.metric(
    "Top Category",
    top_category
)

col3.metric(
    "Categories",
    num_categories
)

st.markdown("---")

# -------------------------
# Category Revenue
# -------------------------

category_rev = (
    df.groupby("product_category")["revenue"]
      .sum()
      .reset_index()
)

category_rev["Revenue Share %"] = (
    category_rev["revenue"]
    / category_rev["revenue"].sum()
    * 100
)

# -------------------------
# Donut Chart
# -------------------------

st.subheader("🍩 Revenue Share by Category")

fig1 = px.pie(
    category_rev,
    names="product_category",
    values="revenue",
    hole=0.6
)

fig1.update_layout(
    height=500
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -------------------------
# Category Revenue Table
# -------------------------

st.subheader("📋 Category Revenue Table")

st.dataframe(
    category_rev.sort_values(
        by="revenue",
        ascending=False
    ),
    use_container_width=True
)

# -------------------------
# Product Type Analysis
# -------------------------

type_rev = (
    df.groupby(
        ["product_category",
         "product_type"]
    )["revenue"]
    .sum()
    .reset_index()
)

# -------------------------
# Sunburst Chart
# -------------------------

st.subheader(
    "☀️ Product Type Contribution"
)

fig2 = px.sunburst(
    type_rev,
    path=[
        "product_category",
        "product_type"
    ],
    values="revenue"
)

fig2.update_layout(
    height=700
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -------------------------
# Treemap
# -------------------------

st.subheader(
    "🌳 Revenue Treemap"
)

fig3 = px.treemap(
    type_rev,
    path=[
        "product_category",
        "product_type"
    ],
    values="revenue"
)

fig3.update_layout(
    height=700
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -------------------------
# Category Performance Table
# -------------------------

st.subheader(
    "📊 Detailed Category Analysis"
)

performance = (
    df.groupby(
        [
            "product_category",
            "product_type"
        ]
    )
    .agg(
        Revenue=("revenue","sum"),
        Units_Sold=("transaction_qty","sum")
    )
    .reset_index()
)

st.dataframe(
    performance,
    use_container_width=True
)

# -------------------------
# Download Report
# -------------------------

csv = performance.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Category Report",
    data=csv,
    file_name="category_analysis.csv",
    mime="text/csv"
)
