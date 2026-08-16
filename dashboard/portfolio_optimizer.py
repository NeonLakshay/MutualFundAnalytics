from pathlib import Path

import streamlit as st

import sqlite3

import numpy as np
import pandas as pd

st.error("🔥 PORTFOLIO OPTIMIZER FILE LOADED")

# ----------------------------------------------------
# Database
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "bluestock_mf.db"


def optimize_portfolio(selected_codes):

    conn = sqlite3.connect(DB_PATH)

    # ---------------------------------------------
    # Load NAV history
    # ---------------------------------------------
    nav_frames = []

    for code in selected_codes:

        query = """
        SELECT
            d.date,
            f.nav
        FROM fact_nav f
        JOIN dim_date d
        ON f.date_id = d.date_id
        WHERE f.amfi_code = ?
        ORDER BY d.date
        """

        df = pd.read_sql(query, conn, params=(int(code),))

        if len(df) == 0:
            continue

        df = df.rename(columns={"nav": str(code)})
        nav_frames.append(df)

    conn.close()

    if len(nav_frames) < 2:
        raise Exception("At least two funds are required.")

    # ---------------------------------------------
    # Merge NAVs
    # ---------------------------------------------
    nav_data = nav_frames[0]

    for df in nav_frames[1:]:
        nav_data = nav_data.merge(df, on="date")

    nav_data = nav_data.drop(columns="date")

    # ---------------------------------------------
    # Daily Returns
    # ---------------------------------------------
    returns = nav_data.pct_change().dropna()

    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252

    # ---------------------------------------------
    # Random Portfolios
    # ---------------------------------------------
    portfolios = 3000

    results = np.zeros((3, portfolios))
    weights_record = []

    for i in range(portfolios):

        weights = np.random.random(len(selected_codes))
        weights /= np.sum(weights)

        portfolio_return = np.sum(mean_returns * weights)

        portfolio_std = np.sqrt(
            np.dot(
                weights.T,
                np.dot(cov_matrix, weights)
            )
        )

        sharpe = portfolio_return / portfolio_std

        results[0, i] = portfolio_std
        results[1, i] = portfolio_return
        results[2, i] = sharpe

        weights_record.append(weights)

    best = np.argmax(results[2])

    return {
        "risk": results[0],
        "return": results[1],
        "sharpe": results[2],
        "best_weights": weights_record[best],
        "best_return": results[1, best],
        "best_risk": results[0, best],
        "best_sharpe": results[2, best]
    }