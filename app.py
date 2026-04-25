import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 🔧 PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Metals Intelligence", layout="wide")

# -----------------------------
# 📥 LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("metal_industry_dataset.csv", parse_dates=["Date"])

df = load_data()

# -----------------------------
# 🎯 HEADER
# -----------------------------
st.markdown("""
# 🪙 Metals & Industry Intelligence Dashboard
Analyze metal prices, industry dependency, and regional insights across India
""")

st.markdown("---")

# -----------------------------
# 🎛️ SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

metal = st.sidebar.selectbox("Metal", ["All"] + sorted(df["Metal"].unique()))
industry = st.sidebar.selectbox("Industry", ["All"] + sorted(df["Industry"].unique()))
state = st.sidebar.selectbox("State", ["All"] + sorted(df["State"].unique()))
region = st.sidebar.selectbox("Region", ["All"] + sorted(df["Region"].unique()))

filtered_df = df.copy()

if metal != "All":
    filtered_df = filtered_df[filtered_df["Metal"] == metal]
if industry != "All":
    filtered_df = filtered_df[filtered_df["Industry"] == industry]
if state != "All":
    filtered_df = filtered_df[filtered_df["State"] == state]
if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]

# -----------------------------
# 📊 KPI SECTION
# -----------------------------
st.subheader("📊 Key Metrics")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Avg Price", f"{filtered_df['Price'].mean():.0f}")
k2.metric("Avg Demand", f"{filtered_df['Demand_Index'].mean():.0f}")
k3.metric("Impact Score", f"{filtered_df['Impact_Score'].mean():.0f}")
k4.metric("Volatility", f"{filtered_df['Volatility'].mean():.3f}")

st.markdown("---")

# -----------------------------
# 📈 SECTION 1: PRICE + METAL
# -----------------------------
st.subheader("📈 Market Trends")

col1, col2 = st.columns(2)

# Price Trend
with col1:
    fig, ax = plt.subplots(figsize=(5,3))
    for m in filtered_df["Metal"].unique():
        subset = filtered_df[filtered_df["Metal"] == m].sort_values("Date")
        ax.plot(subset["Date"], subset["Price"], label=m)
    ax.legend(fontsize=8)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Metal Comparison
with col2:
    fig, ax = plt.subplots(figsize=(5,3))
    filtered_df.groupby("Metal")["Price"].mean().plot(kind="bar", ax=ax)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# -----------------------------
# 🏭 SECTION 2: INDUSTRY
# -----------------------------
st.subheader("🏭 Industry Analysis")

col3, col4 = st.columns(2)

# Industry Impact
with col3:
    fig, ax = plt.subplots(figsize=(5,3))
    filtered_df.groupby("Industry")["Impact_Score"].mean().plot(kind="bar", ax=ax)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Dependency Matrix
with col4:
    pivot = filtered_df.pivot_table(
        index="Industry",
        columns="Metal",
        values="Dependency",
        aggfunc="mean"
    )
    st.dataframe(pivot, use_container_width=True)

st.markdown("---")

# -----------------------------
# 📦 SECTION 3: SUPPLY CHAIN
# -----------------------------
st.subheader("📦 Demand & Supply")

col5, col6 = st.columns(2)

# Demand vs Supply
with col5:
    fig, ax = plt.subplots(figsize=(5,3))
    ax.scatter(filtered_df["Demand_Index"], filtered_df["Supply_Index"])
    ax.set_xlabel("Demand")
    ax.set_ylabel("Supply")
    plt.tight_layout()
    st.pyplot(fig)

# Demand Category
with col6:
    fig, ax = plt.subplots(figsize=(5,3))
    filtered_df["Demand_Category"].value_counts().plot(kind="bar", ax=ax)
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# -----------------------------
# 🌍 SECTION 4: REGION
# -----------------------------
st.subheader("🌍 Regional Insights")

col7, col8 = st.columns(2)

# Region Price
with col7:
    fig, ax = plt.subplots(figsize=(5,3))
    filtered_df.groupby("Region")["Price"].mean().plot(kind="bar", ax=ax)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# State Price
with col8:
    fig, ax = plt.subplots(figsize=(5,3))
    filtered_df.groupby("State")["Price"].mean().sort_values(ascending=False).head(10).plot(kind="bar", ax=ax)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# -----------------------------
# 💡 INSIGHTS
# -----------------------------
st.subheader("💡 Key Insights")

top_industry = filtered_df.groupby("Industry")["Impact_Score"].mean().idxmax()
top_metal = filtered_df.groupby("Metal")["Price"].mean().idxmax()

st.info(f"🏭 Highest Impact Industry: **{top_industry}**")
st.info(f"🪙 Highest Value Metal: **{top_metal}**")

if filtered_df["Volatility"].mean() > 0.05:
    st.warning("⚠️ Market is highly volatile")
else:
    st.success("✅ Market is relatively stable")

# -----------------------------
# 📄 RAW DATA
# -----------------------------
with st.expander("📄 View Data"):
    st.dataframe(filtered_df.head(100), use_container_width=True)