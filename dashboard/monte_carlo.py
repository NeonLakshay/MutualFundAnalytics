from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "db" / "bluestock_mf.db"


def run_monte_carlo(amfi_code):

    # Create fresh database connection
    print("=" * 80)
    print("USING DATABASE:")
    print(DB_PATH)
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM fact_nav
    WHERE amfi_code = ?
    """
    print("AMFI VALUE :", amfi_code)
    print("AMFI TYPE  :", type(amfi_code))

    df = pd.read_sql(
    query,
    conn,
    params=(int(amfi_code),)
    )
    print("=" * 80)
    print("Database :", DB_PATH)
    print("AMFI :", amfi_code)
    print("Columns :", df.columns.tolist())
    print("Rows :", len(df))
    print(df.head())
    print("=" * 80)
    print("Rows returned:", len(df))
    print(df.head())
    print("=" * 60)
    print("DB PATH :", DB_PATH)
    print("AMFI CODE RECEIVED :", amfi_code)
    print("ROWS FOUND :", len(df))
    print(df.head())
    print("=" * 60)
    conn.close()

    # Safety check 1
    if df.empty:
        raise Exception(f"No NAV history found for AMFI Code {amfi_code}")

    nav = df["nav"].astype(float).values

    # Safety check 2
    if len(nav) < 2:
        raise Exception("Not enough NAV history to run simulation.")

    # Daily returns
    returns = np.diff(nav) / nav[:-1]

    # Safety check 3
    returns = returns[np.isfinite(returns)]

    if len(returns) == 0:
        raise Exception("Daily returns are empty.")

    mu = float(np.mean(returns))
    sigma = float(np.std(returns))

    # Safety check 4
    if sigma == 0:
        sigma = 0.01

    S0 = float(nav[-1])

    days = 252 * 5
    simulations = 50

    paths = np.zeros((days, simulations))

    for j in range(simulations):

        prices = [S0]

        for _ in range(days - 1):

            shock = np.random.normal(mu, sigma)

            prices.append(prices[-1] * (1 + shock))

        paths[:, j] = prices

    return paths