import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("metal_industry_dataset.csv", parse_dates=["Date"])

# -------------------------------
# 🔍 BASIC DATA OVERVIEW
# -------------------------------

print("\n📌 Dataset Shape (Rows, Columns):")
print(df.shape)

print("\n📌 Column Names:")
print(df.columns.tolist())

print("\n📌 Data Types:")
print(df.dtypes)

print("\n📌 First 5 Rows:")
print(df.head())

print("\n📌 Last 5 Rows:")
print(df.tail())

# -------------------------------
# ❗ MISSING VALUES
# -------------------------------
print("\n📌 Missing Values:")
print(df.isnull().sum())

# -------------------------------
# 🔁 DUPLICATE DATA
# -------------------------------
duplicates = df.duplicated().sum()
print(f"\n📌 Duplicate Rows: {duplicates}")

# Remove duplicates (optional)
df = df.drop_duplicates()

# -------------------------------
# 📊 BASIC STATISTICS
# -------------------------------
print("\n📌 Statistical Summary:")
print(df.describe())

# -------------------------------
# 📊 GROUPED INSIGHTS
# -------------------------------
print("\n📌 Average Price by Metal:")
print(df.groupby("Metal")["Price"].mean())

print("\n📌 Average Impact by Industry:")
print(df.groupby("Industry")["Impact_Score"].mean())

# -------------------------------
# 🎨 VISUALIZATIONS
# -------------------------------

plt.style.use("default")

# -------------------------------
# 📈 GRAPH 1: Metal Price Trends Over Time
# -------------------------------
plt.figure()
for metal in df["Metal"].unique():
    subset = df[df["Metal"] == metal].sort_values("Date")
    plt.plot(subset["Date"], subset["Price"], label=metal)

plt.title("Metal Price Trends Over Time")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# -------------------------------
# 📊 GRAPH 2: Average Price by Metal
# -------------------------------
plt.figure()
df.groupby("Metal")["Price"].mean().plot(kind="bar")

plt.title("Average Price by Metal")
plt.xlabel("Metal")
plt.ylabel("Average Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# -------------------------------
# 📊 GRAPH 3: Industry Impact Score
# -------------------------------
plt.figure()
df.groupby("Industry")["Impact_Score"].mean().plot(kind="bar")

plt.title("Average Industry Impact Score")
plt.xlabel("Industry")
plt.ylabel("Impact Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# -------------------------------
# 📊 GRAPH 4: Demand vs Supply
# -------------------------------
plt.figure()
plt.scatter(df["Demand_Index"], df["Supply_Index"])

plt.title("Demand vs Supply Distribution")
plt.xlabel("Demand Index")
plt.ylabel("Supply Index")
plt.tight_layout()
plt.show()


# -------------------------------
# 📊 GRAPH 5: Volatility by Metal
# -------------------------------
plt.figure()
df.groupby("Metal")["Volatility"].mean().plot(kind="bar")

plt.title("Average Volatility by Metal")
plt.xlabel("Metal")
plt.ylabel("Volatility")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# -------------------------------
# 📊 GRAPH 6: State-wise Price
# -------------------------------
plt.figure()
df.groupby("State")["Price"].mean().plot(kind="bar")

plt.title("Average Metal Price by State")
plt.xlabel("State")
plt.ylabel("Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------------------
# 📊 NEW GRAPH: Region-wise Price
# ---------------------------
df.groupby("Region")["Price"].mean().plot(kind="bar")
plt.title("Average Metal Price by Region (India)")
plt.xticks(rotation=45)
plt.show()