import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from tabulate import tabulate
import joblib
import kagglehub
path = kagglehub.dataset_download("raminhuseyn/demand-forecasting-dataset")

df=pd.read_csv(f"{path}/demand_forecasting.csv")
df.head()

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

DATA = f"{path}/demand_forecasting.csv"
OUT  = "/mnt/user-data/outputs/"

os.makedirs(OUT, exist_ok=True)

# 1. LOAD
print("Loading dataset …")
df = pd.read_csv(DATA, parse_dates=["Date"])

# 2. CLEAN
df.dropna(subset=["Date", "Demand", "Price"], inplace=True)
df = df[df["Demand"] > 0]
df = df[df["Price"]  > 0]
df["Revenue"]  = df["Demand"] * df["Price"]
df["Month"]    = df["Date"].dt.to_period("M").dt.to_timestamp()
df["YearMonth"]= df["Date"].dt.strftime("%b %Y")

print(f"  Rows after cleaning : {len(df):,}")
print(f"  Date range          : {df['Date'].min().date()} → {df['Date'].max().date()}")
print(f"  Stores              : {df['Store ID'].nunique()}")
print(f"  Products            : {df['Product ID'].nunique()}")
print(f"  Categories          : {df['Category'].nunique()}")

# 3. SUMMARY
print("\nSummary Statistics ")
print(df[["Demand", "Price", "Revenue", "Discount", "Inventory Level"]].describe().round(2).to_string())

promo_lift = df.groupby("Promotion")["Demand"].mean()
print(f"\n  Avg demand WITHOUT promotion : {promo_lift.get(0, 0):.1f}")
print(f"  Avg demand WITH    promotion : {promo_lift.get(1, 0):.1f}")

# 4. CHARTS
sns.set_theme(style="whitegrid", font="DejaVu Sans")
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False})
VIBRANT_BLUE = "#007ACC"
VIBRANT_ORANGE = "#FF8C00"
VIBRANT_GREEN = "#32CD32"
VIBRANT_RED = "#DC143C"

# Chart 1 : Monthly Revenue Trend (all stores combined)
monthly = df.groupby("Month")["Revenue"].sum().reset_index()

fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(monthly["Month"], monthly["Revenue"] / 1_000,
        color=VIBRANT_BLUE, linewidth=2.5, marker="o", markersize=5, zorder=3)
ax.fill_between(monthly["Month"], monthly["Revenue"] / 1_000,
                alpha=0.2, color=VIBRANT_BLUE)
# annotate peak
peak = monthly.loc[monthly["Revenue"].idxmax()]
ax.annotate(f"Peak\n${peak['Revenue']/1_000:,.0f}k",
            xy=(peak["Month"], peak["Revenue"] / 1_000),
            xytext=(10, 15), textcoords="offset points",
            fontsize=8, color=VIBRANT_BLUE, arrowprops=dict(arrowstyle="->", color=VIBRANT_BLUE))

ax.set_title("Monthly Revenue Trend (Jan 2022 – Jan 2024)", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Month"); ax.set_ylabel("Revenue ($k)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}k"))
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig(OUT + "chart1_monthly_revenue.png", dpi=150)
plt.show()
plt.close()

# Chart 2 : Average Demand by Category & Promotion Status
cat_promo = (df.groupby(["Category", "Promotion"])["Demand"]
               .mean()
               .reset_index())
cat_promo["Promotion Label"] = cat_promo["Promotion"].map({0: "No Promotion", 1: "With Promotion"})

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=cat_promo, x="Category", y="Demand",
            hue="Promotion Label",
            palette={"No Promotion": VIBRANT_GREEN, "With Promotion": VIBRANT_BLUE},
            ax=ax, edgecolor="white", width=0.6)
ax.set_title("Average Demand by Category — Promotion Effect", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Category"); ax.set_ylabel("Avg Demand (units)")
ax.legend(title="")
plt.tight_layout()
plt.savefig(OUT + "chart2_demand_by_category_promotion.png", dpi=150)
plt.show()
plt.close()

# Chart 3 : Seasonal Demand Heatmap (Region × Season)
pivot = (df.groupby(["Region", "Seasonality"])["Demand"]
           .mean()
           .unstack()
           .reindex(columns=["Winter", "Spring", "Summer", "Fall"]))

fig, ax = plt.subplots(figsize=(9, 4))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu",
            linewidths=0.5, linecolor="white",
            cbar_kws={"label": "Avg Demand"}, ax=ax)
ax.set_title("Average Demand Heatmap — Region × Season", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Season"); ax.set_ylabel("Region")
plt.tight_layout()
plt.savefig(OUT + "chart3_seasonal_heatmap.png", dpi=150)
plt.show()
plt.close()
