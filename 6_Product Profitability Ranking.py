import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Product Profitability Ranking",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Product Profitability Ranking")
st.markdown(
    "Analyze revenue, profit, and margin performance across products."
)

# =====================================
# Load Data
# =====================================

df = load_data()

# =====================================
# Create Profitability Metrics
# =====================================

# Estimated Cost (65% of revenue)
df["estimated_cost"] = df["revenue"] * 0.65

# Profit
df["profit"] = (
    df["revenue"]
    - df["estimated_cost"]
)

# Profit Margin %
df["profit_margin_pct"] = (
    df["profit"]
    / df["revenue"]
) * 100

# =====================================
# Sidebar Filters
# =====================================

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["product_category"].unique())
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

# =====================================
# Apply Filters
# =====================================

filtered_df = df.copy()

if category:
    filtered_df = filtered_df[
        filtered_df["product_category"].isin(category)
    ]

if location:
    filtered_df = filtered_df[
        filtered_df["store_location"].isin(location)
    ]

# =====================================
# KPI Calculations
# =====================================

total_revenue = filtered_df["revenue"].sum()

total_profit = filtered_df["profit"].sum()

avg_margin = (
    filtered_df["profit_margin_pct"]
    .mean()
)

total_products = (
    filtered_df["product_detail"]
    .nunique()
)

# =====================================
# KPI Cards
# =====================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"{total_revenue:,.0f}"
)

col2.metric(
    "Total Profit",
    f"{total_profit:,.0f}"
)

col3.metric(
    "Avg Margin %",
    f"{avg_margin:.1f}%"
)

col4.metric(
    "Products",
    total_products
)

st.markdown("---")

# =====================================
# Product Profitability Summary
# =====================================

product_perf = (
    filtered_df
    .groupby("product_detail")
    .agg(
        Revenue=("revenue", "sum"),
        Profit=("profit", "sum"),
        Units_Sold=("transaction_qty", "sum")
    )
    .reset_index()
)

product_perf["Profit Margin %"] = (
    product_perf["Profit"]
    / product_perf["Revenue"]
) * 100

# =====================================
# Top Profit Products
# =====================================

st.subheader("🏆 Top Products by Profit")

top_profit = (
    product_perf
    .sort_values(
        by="Profit",
        ascending=False
    )
    .head(top_n)
)

fig = px.bar(
    top_profit,
    x="Profit",
    y="product_detail",
    orientation="h",
    text_auto=".2s",
    title=f"Top {top_n} Products by Profit"
)

fig.update_layout(
    yaxis_title="Product",
    xaxis_title="Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# Revenue vs Profit Scatter Plot
# =====================================

st.subheader("📊 Revenue vs Profit Analysis")

fig2 = px.scatter(
    product_perf,
    x="Revenue",
    y="Profit",
    size="Units_Sold",
    hover_name="product_detail",
    color="Profit Margin %",
    title="Revenue vs Profit Performance"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================
# Profitability Ranking Table
# =====================================

st.subheader("📋 Product Profitability Ranking")

ranking_table = (
    product_perf
    .sort_values(
        by="Profit",
        ascending=False
    )
)

st.dataframe(
    ranking_table,
    use_container_width=True
)

# =====================================
# Business Insights
# =====================================

st.subheader("📌 Business Insights")

top5_share = (
    ranking_table.head(5)["Profit"].sum()
    /
    ranking_table["Profit"].sum()
) * 100

st.info(
    f"""
    • Top 5 products contribute approximately
    {top5_share:.1f}% of total profit.

    • Products with high revenue but low profit
    margins may require pricing review.

    • Products with low revenue and low profit
    are potential candidates for menu optimization.

    • Focus marketing efforts on high-profit,
    high-volume products.
    """
)