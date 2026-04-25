import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
np.random.seed(42)
random.seed(42)

NUM_ROWS = 50000

metals = ["Gold", "Silver", "Copper", "Aluminum", "Lithium", "Nickel", "Steel", "Platinum"]
industries = ["Construction", "Automobile", "Electronics", "Energy", "Jewelry"]

# -------------------------------
# 🇮🇳 India States + Regions Mapping
# -------------------------------
state_region_map = {
    "Andhra Pradesh": "South", "Arunachal Pradesh": "Northeast",
    "Assam": "Northeast", "Bihar": "East",
    "Chhattisgarh": "Central", "Goa": "West",
    "Gujarat": "West", "Haryana": "North",
    "Himachal Pradesh": "North", "Jharkhand": "East",
    "Karnataka": "South", "Kerala": "South",
    "Madhya Pradesh": "Central", "Maharashtra": "West",
    "Manipur": "Northeast", "Meghalaya": "Northeast",
    "Mizoram": "Northeast", "Nagaland": "Northeast",
    "Odisha": "East", "Punjab": "North",
    "Rajasthan": "North", "Sikkim": "Northeast",
    "Tamil Nadu": "South", "Telangana": "South",
    "Tripura": "Northeast", "Uttar Pradesh": "North",
    "Uttarakhand": "North", "West Bengal": "East",
    # Union Territories
    "Delhi": "North", "Jammu and Kashmir": "North",
    "Ladakh": "North", "Chandigarh": "North",
    "Puducherry": "South", "Andaman and Nicobar Islands": "South",
    "Lakshadweep": "South", "Dadra and Nagar Haveli and Daman and Diu": "West"
}

states = list(state_region_map.keys())
regions = ["North", "South", "East", "West"]

base_prices = {
    "Gold": 5000, "Silver": 60, "Copper": 800, "Aluminum": 200,
    "Lithium": 3000, "Nickel": 1500, "Steel": 100, "Platinum": 4000
}

trend_factor = {
    "Gold": 0.0002, "Silver": 0.0005, "Copper": 0.0003,
    "Aluminum": 0.0001, "Lithium": 0.001, "Nickel": 0.0007,
    "Steel": 0.0002, "Platinum": 0.0003
}

dependency_map = {
    "Construction": {"Steel": 0.95, "Aluminum": 0.85, "Copper": 0.5},
    "Automobile": {"Steel": 0.8, "Aluminum": 0.7, "Copper": 0.6, "Nickel": 0.5},
    "Electronics": {"Copper": 0.9, "Gold": 0.85, "Silver": 0.75},
    "Energy": {"Lithium": 0.95, "Nickel": 0.85, "Copper": 0.6},
    "Jewelry": {"Gold": 0.98, "Silver": 0.9, "Platinum": 0.85}
}

data = []

for _ in range(NUM_ROWS):
    date = fake.date_between(start_date="-3y", end_date="today")
    metal = random.choice(metals)
    industry = random.choice(industries)
    state = random.choice(states)
    region = random.choice(regions)

    base_price = base_prices[metal]
    days = (pd.Timestamp.today() - pd.Timestamp(date)).days

    trend = base_price * (1 + trend_factor[metal] * days)
    seasonal = base_price * 0.1 * np.sin(2 * np.pi * days / 365)
    noise = np.random.normal(0, base_price * 0.05)

    shock = base_price * random.uniform(-0.4, 0.6) if random.random() < 0.03 else 0

    price = max(1, trend + seasonal + noise + shock)
    
    # Regional price multiplier (realistic variation)
    region_multiplier = {
        "North": 1.02,
        "South": 1.03,
        "East": 0.98,
        "West": 1.01,
        "Central": 0.99,
        "Northeast": 1.05
    }

    region = state_region_map[state]

    price = price * region_multiplier[region]

    dependency = dependency_map.get(industry, {}).get(metal, random.uniform(0.2, 0.5))

    demand_index = random.uniform(50, 200) * dependency
    supply_index = random.uniform(50, 150)

    impact_score = price * dependency
    volatility = abs(noise) / base_price

    # NEW FEATURES
    is_primary = 1 if dependency > 0.85 else 0

    if dependency > 0.85:
        demand_category = "High"
    elif dependency > 0.6:
        demand_category = "Medium"
    else:
        demand_category = "Low"

    price_trend = "Rising" if trend_factor[metal] > 0 else "Falling"

    data.append([
        date, metal, industry, state, region,
        round(price, 2),
        round(demand_index, 2),
        round(supply_index, 2),
        round(dependency, 2),
        round(impact_score, 2),
        round(volatility, 4),
        is_primary,
        demand_category,
        price_trend
    ])

df = pd.DataFrame(data, columns=[
    "Date","Metal","Industry","State","Region",
    "Price","Demand_Index","Supply_Index",
    "Dependency","Impact_Score","Volatility",
    "Primary_Metal","Demand_Category","Price_Trend"
])

df = df.sort_values("Date")
df.to_csv("metal_industry_dataset.csv", index=False)

print("✅ Dataset Generated:", df.shape)