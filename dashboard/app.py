from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go

from monte_carlo import run_monte_carlo
from portfolio_optimizer import optimize_portfolio

from textwrap import dedent

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Bluestock Mutual Fund Analytics",
    page_icon="📈",
    layout="wide"
)

# ----------------------------------------------------
# Custom CSS
# ----------------------------------------------------
st.markdown("""
<style>
.main {
    background-color:#F8FAFC;
}

.kpi-card{
    background:white;
    padding:18px;
    border-radius:12px;
    border:1px solid #E5E7EB;
    box-shadow:0px 3px 8px rgba(0,0,0,0.08);
    text-align:center;
}

.metric-title{
    color:#6B7280;
    font-size:15px;
}

.metric-value{
    color:#2563EB;
    font-size:30px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Database Connection
# ----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "bluestock_mf.db"

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_connection()

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------
st.sidebar.image(
    "https://img.icons8.com/color/96/combo-chart--v1.png",
    width=80
)

st.sidebar.title("Bluestock Analytics")

st.sidebar.caption(
    "Professional Mutual Fund Analytics Dashboard"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "NAV Analytics",
        "Performance",
        "Investor Analytics",
        "Fund Explorer"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    Mutual Fund Analytics

    Built with:

    • Streamlit
    • SQLite
    • Plotly
    • Python
    """
)

# ----------------------------------------------------
# Dashboard Header
# ----------------------------------------------------
st.title("📊 Bluestock Mutual Fund Analytics Dashboard")

st.caption(
    "Interactive Mutual Fund Analytics powered by SQLite and Streamlit"
)

# ----------------------------------------------------
# KPI Queries
# ----------------------------------------------------
total_funds = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM dim_fund",
    conn
).iloc[0]["cnt"]

total_nav = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM fact_nav",
    conn
).iloc[0]["cnt"]

total_transactions = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM fact_transactions",
    conn
).iloc[0]["cnt"]

avg_return = pd.read_sql(
    """
    SELECT ROUND(AVG(return_3yr_pct),2) AS avg_return
    FROM fact_performance
    """,
    conn
).iloc[0]["avg_return"]

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="metric-title">Total Funds</div>
        <div class="metric-value">{total_funds}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="metric-title">NAV Records</div>
        <div class="metric-value">{total_nav:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="metric-title">Transactions</div>
        <div class="metric-value">{total_transactions:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="metric-title">Avg 3-Year Return</div>
        <div class="metric-value">{avg_return}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# st.success("✅ Database connected successfully.")

# ==========================================================
# INTERACTIVE ANALYTICS
# ==========================================================

st.markdown("---")
st.header("📈 Interactive Analytics")

# ----------------------------------------------------------
# NAV Trend
# ----------------------------------------------------------

nav_df = pd.read_sql("""
SELECT
d.date,
AVG(f.nav) AS avg_nav
FROM fact_nav f
JOIN dim_date d
ON f.date_id=d.date_id
GROUP BY d.date
ORDER BY d.date
""", conn)

# ----------------------------------------------------------
# Top Performing Funds
# ----------------------------------------------------------

performance_df = pd.read_sql("""
SELECT
scheme_name,
return_3yr_pct
FROM fact_performance p
JOIN dim_fund f
ON p.amfi_code=f.amfi_code
ORDER BY return_3yr_pct DESC
LIMIT 10
""", conn)

# ----------------------------------------------------------
# Transaction Distribution
# ----------------------------------------------------------

transaction_df = pd.read_sql("""
SELECT
transaction_type,
COUNT(*) AS total
FROM fact_transactions
GROUP BY transaction_type
""", conn)

# ----------------------------------------------------------
# Top States
# ----------------------------------------------------------

state_df = pd.read_sql("""
SELECT
state,
COUNT(*) AS investors
FROM fact_transactions
GROUP BY state
ORDER BY investors DESC
LIMIT 10
""", conn)

# ----------------------------------------------------------
# Morningstar Rating
# ----------------------------------------------------------

rating_df = pd.read_sql("""
SELECT
morningstar_rating,
COUNT(*) AS total
FROM fact_performance
GROUP BY morningstar_rating
ORDER BY morningstar_rating
""", conn)

# ==========================================================
# CHARTS
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    fig1 = px.line(
        nav_df,
        x="date",
        y="avg_nav",
        title="Average NAV Trend",
        markers=False
    )

    fig1.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    fig2 = px.bar(
        performance_df,
        x="return_3yr_pct",
        y="scheme_name",
        orientation="h",
        title="Top 10 Performing Funds",
        color="return_3yr_pct"
    )

    fig2.update_layout(
        template="plotly_white",
        height=450,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==========================================================

col3, col4 = st.columns(2)

with col3:

    fig3 = px.pie(
        transaction_df,
        names="transaction_type",
        values="total",
        hole=0.45,
        title="Transaction Distribution"
    )

    fig3.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:

    fig4 = px.bar(
        state_df,
        x="state",
        y="investors",
        title="Top States by Investors",
        color="investors"
    )

    fig4.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig4, use_container_width=True)

# ==========================================================

fig5 = px.bar(
    rating_df,
    x="morningstar_rating",
    y="total",
    title="Morningstar Rating Distribution",
    color="total"
)

fig5.update_layout(
    template="plotly_white",
    height=450
)

st.plotly_chart(fig5, use_container_width=True)

# ==========================================================

st.markdown("---")

# st.success("🎉 Interactive Dashboard Loaded Successfully!")


st.markdown("---")
st.header("🔍 Fund Explorer")

funds = pd.read_sql("""
SELECT
amfi_code,
scheme_name,
fund_house,
category,
plan,
risk_grade
FROM dim_fund
ORDER BY scheme_name
""", conn)

selected_fund = st.selectbox(
    "Select Mutual Fund",
    funds["scheme_name"]
)

# Get selected fund information
fund_info = funds[funds["scheme_name"] == selected_fund]

# Get AMFI Code
selected_code = int(fund_info.iloc[0]["amfi_code"])

st.write("Selected Code:", selected_code)

st.dataframe(
    fund_info,
    use_container_width=True,
    hide_index=True
)

csv = fund_info.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Fund Details",
    csv,
    file_name="fund_details.csv",
    mime="text/csv"
)

st.markdown("---")
st.subheader("Monte Carlo Simulation")

if st.button("Run 5-Year Forecast"):
    st.write("Selected Code:", selected_code)
    paths = run_monte_carlo(selected_code)
    mean_path = paths.mean(axis=1)
    fig = go.Figure()

    for i in range(50):
        fig.add_trace(
            go.Scatter(
                y=paths[:, i],
                mode="lines",
                line=dict(width=1),
                opacity=0.25,
                showlegend=False
            )
        )

    fig.add_trace(
        go.Scatter(
            y=mean_path,
            mode="lines",
            name="Expected NAV",
            line=dict(width=4, color="red")
       )
    )    

    fig.update_layout(
        title="Monte Carlo NAV Projection",
        xaxis_title="Trading Days",
        yaxis_title="Projected NAV"
    )

    st.plotly_chart(fig, use_container_width=True)


st.markdown("---")

st.markdown("")
st.header("📈 Portfolio Optimizer")

fund_list = pd.read_sql("""
SELECT
    amfi_code,
    scheme_name
FROM dim_fund
ORDER BY scheme_name
""", conn)

selected_funds = st.multiselect(
    "Select exactly 5 Mutual Funds",
    fund_list["scheme_name"].tolist(),
    max_selections=5
)

if len(selected_funds) == 5:

    selected_codes = []

    for fund in selected_funds:
        code = fund_list.loc[
            fund_list["scheme_name"] == fund,
            "amfi_code"
        ].iloc[0]

        selected_codes.append(int(code))

if st.button("🚀 Optimize Portfolio"):

    result = optimize_portfolio(selected_codes)

    st.success("✅ Portfolio Optimized Successfully!")

    weights_df = pd.DataFrame({
        "Fund": selected_funds,
        "Weight (%)": (result["best_weights"] * 100).round(2)
    })

    # Two-column layout
    left_col, right_col = st.columns([3, 1])

    # ===========================
    # LEFT COLUMN
    # ===========================
    with left_col:

        fig = px.scatter(
            x=result["risk"],
            y=result["return"],
            color=result["sharpe"],
            labels={
                "x": "Risk",
                "y": "Expected Return",
                "color": "Sharpe"
            },
            title="Efficient Frontier"
        )

        fig.add_scatter(
            x=[result["best_risk"]],
            y=[result["best_return"]],
            mode="markers",
            marker=dict(
                size=16,
                color="red",
                symbol="star"
            ),
            name="Optimal Portfolio"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="efficient_frontier"
        )

    # ===========================
    # RIGHT COLUMN
    # ===========================
    with right_col:

        st.subheader("⭐ Optimal Allocation")

        st.dataframe(
            weights_df,
            use_container_width=True,
            hide_index=True
        )

        pie = px.pie(
            weights_df,
            names="Fund",
            values="Weight (%)",
            hole=0.45,
            title="Portfolio Allocation"
        )

        st.plotly_chart(
            pie,
            use_container_width=True,
            key="allocation_pie"
        )

        st.metric(
            "Expected Return",
            f"{result['best_return']*100:.2f}%"
        )

        st.metric(
            "Portfolio Risk",
            f"{result['best_risk']*100:.2f}%"
        )

        st.metric(
            "Sharpe Ratio",
            f"{result['best_sharpe']:.2f}"
        )

else:
    st.info("Please select exactly 5 mutual funds.")

st.markdown("---")

st.markdown(
    """
<div style="text-align:center; padding:25px; margin-top:40px; color:#9CA3AF; font-size:15px; border-top:1px solid #2D3748;">

<h4 style="color:white; margin-bottom:8px;">
📊 Bluestock Mutual Fund Analytics
</h4>

<p style="margin:4px;">
Developed with ❤️ using <b>Python</b> • <b>SQLite</b> • <b>Streamlit</b> • <b>Plotly</b>
</p>

<p style="margin-top:12px; font-size:13px;">
© 2026 Bluestock Fintech Capstone Project
</p>

</div>
""",
    unsafe_allow_html=True,
)