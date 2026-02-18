import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt


# --------------------------
# Connexion à DuckDB
# --------------------------
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "data" / "warehouse.duckdb"

print("DB utilisée :", DB_PATH)

con = duckdb.connect(str(DB_PATH), read_only=True)


# --------------------------
# Charger les tables
# --------------------------
df_monthly = con.execute("SELECT * FROM mart_monthly_revenue").df()
df_product = con.execute("""
SELECT *
FROM mart_product_performance
ORDER BY revenue DESC
LIMIT 10
""").df()


df_client = con.execute("""
SELECT *
FROM mart_customer_performance
ORDER BY total_spent DESC
LIMIT 10
""").df()


# --------------------------
# Préparer date pour df_monthly
# --------------------------
df_monthly['date'] = pd.to_datetime(df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str) + '-01')

# --------------------------
# Streamlit layout
# --------------------------
st.title("Mini Dashboard E-commerce")

st.header("1️⃣ Evolution du chiffre d'affaires")
fig, ax = plt.subplots(figsize=(12,5))
ax.plot(df_monthly['date'], df_monthly['revenue'], marker='o')
ax.set_xlabel("Date (Année-Mois)")
ax.set_ylabel("Revenue")
ax.set_title("Évolution du CA")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

st.header("2️⃣ Top 10 produits par CA")
fig, ax = plt.subplots(figsize=(10,6))
ax.barh(df_product['Description'], df_product['revenue'], color='skyblue')
ax.set_xlabel("Revenue")
ax.set_ylabel("Produit")
ax.set_title("Top produits")
ax.invert_yaxis()
st.pyplot(fig)

st.header("3️⃣ Top 10 clients par CA")
fig, ax = plt.subplots(figsize=(10,6))
ax.barh(df_client['Customer ID'].astype(str), df_client['total_spent'], color='lightgreen')
ax.set_xlabel("Revenue")
ax.set_ylabel("Client")
ax.set_title("Top clients")
ax.invert_yaxis()
st.pyplot(fig)

st.header("4️⃣ Nombre de commandes mensuelles")
fig, ax = plt.subplots(figsize=(12,5))
ax.bar(df_monthly['date'], df_monthly['nb_orders'], color='orange')
ax.set_xlabel("Date")
ax.set_ylabel("Nombre de commandes")
ax.set_title("Commandes mensuelles")
plt.xticks(rotation=45)
plt.grid(axis='y')
st.pyplot(fig)
