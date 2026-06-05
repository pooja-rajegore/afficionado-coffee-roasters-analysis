import streamlit as st

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Afficionado Coffee Analytics",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# Custom CSS
# -----------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

h1 {
    color: #6F4E37;
}

.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Header
# -----------------------------------

st.title("☕ Afficionado Coffee Roasters")

st.subheader(
    "Product Optimization & Revenue Contribution Analysis"
)

st.markdown("---")

# -----------------------------------
# Project Overview
# -----------------------------------

st.markdown("""
## 📖 Project Overview

This dashboard helps Afficionado Coffee Roasters understand:

- Which products customers prefer
- Which products generate the most revenue
- Revenue contribution by category and product type
- Revenue concentration across the menu
- High-performing and low-performing products
- Product popularity vs profitability

The dashboard supports menu optimization and business decision-making.
""")

# -----------------------------------
# Business Objectives
# -----------------------------------

st.markdown("""
## 🎯 Business Objectives

### Primary Objectives

✅ Identify top-selling and least-selling products

✅ Measure revenue contribution by product

✅ Measure revenue contribution by category

✅ Analyze menu revenue concentration

✅ Compare popularity vs profitability

### Secondary Objectives

✅ Support menu simplification

✅ Identify hero products

✅ Highlight underperforming products

✅ Reduce menu complexity

✅ Improve revenue optimization
""")

# -----------------------------------
# Dashboard Navigation
# -----------------------------------

st.markdown("---")

st.markdown("""
## 📊 Dashboard Pages

Use the left sidebar to navigate through the analysis.

### 1️⃣ Executive Summary
- KPI Cards
- Revenue Overview
- Business Performance Snapshot

### 2️⃣ Product Ranking
- Top Products by Revenue
- Top Products by Units Sold
- Product Performance Ranking

### 3️⃣ Category Analysis
- Revenue Share by Category
- Product-Type Contribution
- Category Dependency Analysis

### 4️⃣ Popularity vs Revenue
- Scatter Plot Analysis
- Hero Product Identification
- Underperforming Product Detection

### 5️⃣ Product Drill-Down
- Product-Level KPIs
- Store-Level Performance
- Transaction Details
""")

# -----------------------------------
# Footer
# -----------------------------------

st.markdown("---")

st.markdown("""
### 👨‍💻 Developed By

**Pooja Rajegore**

Data Analytics Project

**Tools Used**
- Python
- Pandas
- PostgreSQL
- Streamlit
- Plotly
- Excel
""")