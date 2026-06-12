import streamlit as st

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Afficionado Coffee Analytics",
    page_icon="☕",
    layout="wide"
)

# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

.main {
    background-color: #faf8f5;
}

.hero {
    padding: 2rem;
    border-radius: 15px;
    background: linear-gradient(
        90deg,
        #6F4E37,
        #A67B5B
    );
    color: white;
}

.metric-box {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ==================================
# HERO SECTION
# ==================================

st.markdown("""
<div class="hero">

# ☕ Afficionado Coffee Roasters Analytics Dashboard

### Product Optimization, Revenue Contribution &
### Profitability Analysis

This interactive business intelligence dashboard helps
stakeholders analyze product performance, revenue trends,
profitability, category contribution, and menu optimization
opportunities.

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================================
# PROJECT OVERVIEW
# ==================================

st.subheader("📌 Project Overview")

st.write("""
This project analyzes coffee retail transaction data to identify:

- Best-selling products
- Revenue-driving products
- Category-level revenue contribution
- Product popularity vs profitability
- Cost and profit analysis
- Menu optimization opportunities
- Revenue concentration risks

The dashboard was built using:

**Python • SQL • PostgreSQL • Streamlit • Plotly • Pandas**
""")

st.markdown("---")

# ==================================
# DASHBOARD MODULES
# ==================================

st.subheader("📊 Dashboard Modules")

col1, col2 = st.columns(2)

with col1:

    st.info("""
    📈 Executive Summary

    - Revenue KPIs
    - Sales KPIs
    - Product KPIs
    - Business Overview
    """)

    st.info("""
    🏆 Product Ranking

    - Top Products
    - Bottom Products
    - Revenue Ranking
    - Volume Ranking
    """)

    st.info("""
    📂 Category Analysis

    - Revenue Distribution
    - Category Contribution
    - Product Type Analysis
    """)

with col2:

    st.info("""
    📊 Popularity vs Revenue

    - Product Comparison
    - Revenue vs Volume
    - Opportunity Analysis
    """)

    st.info("""
    🔎 Product Drilldown

    - Detailed Product Insights
    - Product-Level Performance
    """)

    st.info("""
    💰 Profitability & Cost Analysis

    - Estimated Cost
    - Profit Margin
    - Revenue vs Profit
    - Cost Optimization
    """)

st.markdown("---")

# ==================================
# BUSINESS QUESTIONS
# ==================================

st.subheader("🎯 Key Business Questions")

st.success("""
✔ Which products customers prefer?

✔ Which products generate the most revenue?

✔ Which products generate the most profit?

✔ How revenue is distributed across categories?

✔ Which products should be promoted?

✔ Which products should be reviewed or redesigned?

✔ How concentrated is revenue across the menu?
""")

st.markdown("---")

# ==================================
# PROJECT IMPACT
# ==================================

st.subheader("🚀 Business Impact")

st.write("""
The dashboard enables data-driven decision making by helping:

- Store Managers
- Product Teams
- Business Analysts
- Revenue Managers

identify revenue drivers, optimize menu offerings,
improve profitability, and reduce dependence on
underperforming products.
""")

st.markdown("---")

# ==================================
# SIDEBAR
# ==================================

st.sidebar.success(
    "👈 Select a page from the sidebar"
)

st.sidebar.markdown("""
### Dashboard Pages

☕ Executive Summary

🏆 Product Ranking

📂 Category Analysis

📊 Popularity vs Revenue

🔎 Product Drilldown

💰 Product Profitability

💵 Cost Analysis
""")

# ==================================
# FOOTER
# ==================================

st.markdown("---")

st.caption(
    "Afficionado Coffee Roasters Analytics Dashboard | Built with Streamlit, Python, SQL & PostgreSQL"
)