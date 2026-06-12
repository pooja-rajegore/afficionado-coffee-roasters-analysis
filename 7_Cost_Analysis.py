import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Cost Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Cost & Profitability Analysis")
st.markdown(
    """
    Analyze revenue, estimated costs, profit contribution,
    and product profitability across categories and locations.
    """
)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

# ==========================================
# COST & PROFIT CALCULATIONS
# ==========================================

# Assumption:
# Estimated Cost = 65% of Revenue

df["estimated_cost"] = df["revenue"] * 0.65

df["profit"] = (
    df["revenue"]
    - df["estimated_cost"]
)

df["profit_margin_pct"] = (
    df["profit"]
    / df["revenue"]
) * 100

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Product Category",
    sorted(df["product_category"].unique())
)

location = st.sidebar.multiselect(
    "Store Location",
    sorted(df["store_location"].unique())
)

product_type = st.sidebar.multiselect(
    "Product Type",
    sorted(df["product_type"].unique())
)

# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df.copy()

if category:
    filtered_df = filtered_df[
        filtered_df["product_category"].isin(category)
    ]

if location:
    filtered_df = filtered_df[
        filtered_df["store_location"].isin(location)
    ]

if product_type:
    filtered_df = filtered_df[
        filtered_df["product_type"].isin(product_type)
    ]

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_revenue = filtered_df["revenue"].sum()

total_cost = filtered_df["estimated_cost"].sum()

total_profit = filtered_df["profit"].sum()

profit_margin = (
    total_profit / total_revenue
) * 100

cost_ratio = (
    total_cost / total_revenue
) * 100

# ==========================================
# KPI CARDS
# ==========================================

st.subheader("Executive Summary")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Revenue",
    f"{total_revenue:,.0f}"
)

col2.metric(
    "Cost",
    f"{total_cost:,.0f}"
)

col3.metric(
    "Profit",
    f"{total_profit:,.0f}"
)

col4.metric(
    "Profit Margin %",
    f"{profit_margin:.1f}%"
)

col5.metric(
    "Cost Ratio %",
    f"{cost_ratio:.1f}%"
)

st.markdown("---")

# ==========================================
# REVENUE VS COST BY CATEGORY
# ==========================================

st.subheader("Revenue vs Cost by Category")

category_analysis = (
    filtered_df
    .groupby("product_category")
    .agg(
        Revenue=("revenue", "sum"),
        Cost=("estimated_cost", "sum")
    )
    .reset_index()
)

fig1 = px.bar(
    category_analysis,
    x="product_category",
    y=["Revenue", "Cost"],
    barmode="group",
    title="Revenue and Cost Comparison"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================
# PROFIT BY CATEGORY
# ==========================================

st.subheader("Profit Contribution by Category")

category_profit = (
    filtered_df
    .groupby("product_category")
    .agg(
        Profit=("profit", "sum")
    )
    .reset_index()
)

fig2 = px.pie(
    category_profit,
    names="product_category",
    values="Profit",
    hole=0.5,
    title="Profit Share by Category"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# TOP COSTLY PRODUCTS
# ==========================================

st.subheader("Top 10 Costliest Products")

product_cost = (
    filtered_df
    .groupby("product_detail")
    .agg(
        Revenue=("revenue", "sum"),
        Cost=("estimated_cost", "sum"),
        Profit=("profit", "sum")
    )
    .reset_index()
)

top_costly = (
    product_cost
    .sort_values(
        by="Cost",
        ascending=False
    )
    .head(10)
)

fig3 = px.bar(
    top_costly,
    x="Cost",
    y="product_detail",
    orientation="h",
    text_auto=".2s",
    title="Top Cost-Generating Products"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# REVENUE VS PROFIT SCATTER
# ==========================================

st.subheader("Revenue vs Profit Analysis")

product_profitability = (
    filtered_df
    .groupby("product_detail")
    .agg(
        Revenue=("revenue", "sum"),
        Profit=("profit", "sum"),
        Units_Sold=("transaction_qty", "sum")
    )
    .reset_index()
)

fig4 = px.scatter(
    product_profitability,
    x="Revenue",
    y="Profit",
    size="Units_Sold",
    hover_name="product_detail",
    title="Revenue vs Profit by Product"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# PROFIT MARGIN ANALYSIS
# ==========================================

st.subheader("Top Products by Profit Margin")

margin_analysis = (
    filtered_df
    .groupby("product_detail")
    .agg(
        Revenue=("revenue", "sum"),
        Profit=("profit", "sum")
    )
    .reset_index()
)

margin_analysis["Profit Margin %"] = (
    margin_analysis["Profit"]
    / margin_analysis["Revenue"]
) * 100

top_margin = (
    margin_analysis
    .sort_values(
        by="Profit Margin %",
        ascending=False
    )
    .head(10)
)

fig5 = px.bar(
    top_margin,
    x="Profit Margin %",
    y="product_detail",
    orientation="h",
    title="Top Products by Profit Margin"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ==========================================
# DETAILED TABLE
# ==========================================

st.subheader("Detailed Cost Analysis Table")

detailed_table = (
    product_cost
    .sort_values(
        by="Profit",
        ascending=False
    )
)

st.dataframe(
    detailed_table,
    use_container_width=True
)

# ==========================================
# BUSINESS INSIGHTS
# ==========================================

st.subheader("📌 Key Business Insights")

top5_profit_share = (
    detailed_table.head(5)["Profit"].sum()
    /
    detailed_table["Profit"].sum()
) * 100

st.success(
    f"""
    • Top 5 products contribute approximately {top5_profit_share:.1f}% of total profit.

    • High-revenue products should be monitored for cost efficiency.

    • Products with low profit margins may require pricing optimization.

    • High-cost, low-profit products are potential candidates for menu redesign.

    • Category-level profit analysis helps identify the most profitable business segments.

    • Cost-to-revenue ratio can be used to evaluate overall operational efficiency.
    """
)

st.info(
    """
    Note:
    Cost values are estimated using an assumed cost ratio
    of 65% of revenue for profitability analysis purposes.
    """
)