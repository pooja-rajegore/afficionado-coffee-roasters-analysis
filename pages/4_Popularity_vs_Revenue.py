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

if category:
    df = df[df["product_category"].isin(category)]

if product_type:
    df = df[df["product_type"].isin(product_type)]

if location:
    df = df[df["store_location"].isin(location)]

# -------------------------
# Page Title
# -------------------------

st.title("📈 Popularity vs Revenue Analysis")

st.markdown("""
This analysis compares product popularity (Units Sold)
against Revenue generated.

Use it to identify:

- 🏆 Hero Products
- 📈 Popular but Low Revenue Products
- 💎 Premium Products
- ⚠️ Underperforming Products
""")

st.markdown("---")

# -------------------------
# Product Aggregation
# -------------------------

scatter_df = (
    df.groupby("product_detail")
      .agg(
          Units_Sold=("transaction_qty", "sum"),
          Revenue=("revenue", "sum"),
          Avg_Price=("unit_price", "mean")
      )
      .reset_index()
)

# -------------------------
# KPI Cards
# -------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Products Analyzed",
    scatter_df.shape[0]
)

col2.metric(
    "Total Units Sold",
    f"{scatter_df['Units_Sold'].sum():,.0f}"
)

col3.metric(
    "Total Revenue",
    f"{scatter_df['Revenue'].sum():,.2f}"
)

st.markdown("---")

# -------------------------
# Scatter Plot
# -------------------------

st.subheader("🎯 Popularity vs Revenue Scatter Plot")

fig = px.scatter(
    scatter_df,
    x="Units_Sold",
    y="Revenue",
    size="Revenue",
    color="Revenue",
    hover_name="product_detail",
    hover_data=["Avg_Price"],
    title="Popularity vs Revenue"
)

fig.update_layout(
    height=700,
    xaxis_title="Units Sold",
    yaxis_title="Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------
# Quadrant Explanation
# -------------------------

st.info("""
### Quadrant Interpretation

🏆 Top Right → Hero Products  
High Revenue + High Sales

📈 Top Left → Popular Products  
High Sales + Lower Revenue

💎 Bottom Right → Premium Products  
High Revenue + Lower Sales

⚠️ Bottom Left → Underperforming Products  
Low Revenue + Low Sales
""")

# -------------------------
# Top Hero Products
# -------------------------

st.subheader("🏆 Top Revenue Products")

hero_products = (
    scatter_df
    .sort_values(
        by="Revenue",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    hero_products,
    use_container_width=True
)

# -------------------------
# Underperforming Products
# -------------------------

st.subheader("⚠️ Low Performing Products")

low_products = (
    scatter_df
    .sort_values(
        by=["Revenue", "Units_Sold"]
    )
    .head(10)
)

st.dataframe(
    low_products,
    use_container_width=True
)

# -------------------------
# Revenue vs Units Table
# -------------------------

st.subheader("📋 Product Comparison Table")

st.dataframe(
    scatter_df.sort_values(
        by="Revenue",
        ascending=False
    ),
    use_container_width=True
)

# -------------------------
# Download Report
# -------------------------

csv = scatter_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Analysis Report",
    data=csv,
    file_name="popularity_vs_revenue.csv",
    mime="text/csv"
)
