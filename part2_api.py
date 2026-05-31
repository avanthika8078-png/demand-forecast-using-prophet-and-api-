#Data Summary AI-Generated Plain-English summary

!pip install groq pandas
from groq import Groq
import pandas as pd
import os
import kagglehub
path = kagglehub.dataset_download("raminhuseyn/demand-forecasting-dataset")

df=pd.read_csv(f"{path}/demand_forecasting.csv")
df.head()

DATA = f"{path}/demand_forecasting.csv"

#  INITIALISE CLIENT
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY", "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"),
)
MODEL = "llama-3.3-70b-versatile"

#  1. LOAD & CLEAN
print("Loading dataset …")
df = pd.read_csv(DATA, parse_dates=["Date"])
df["Revenue"] = df["Demand"] * df["Price"]

#  2. COMPUTE SUMMARY STATS
print("Computing summary statistics …\n")

total_rows     = len(df)
date_min       = df["Date"].min().strftime("%d %b %Y")
date_max       = df["Date"].max().strftime("%d %b %Y")
n_stores       = df["Store ID"].nunique()
n_products     = df["Product ID"].nunique()
n_categories   = df["Category"].nunique()
total_units    = int(df["Demand"].sum())
total_revenue  = df["Revenue"].sum()
avg_price      = df["Price"].mean()
avg_demand     = df["Demand"].mean()
promo_demand   = df[df["Promotion"] == 1]["Demand"].mean()
no_promo_demand= df[df["Promotion"] == 0]["Demand"].mean()
promo_lift_pct = (promo_demand - no_promo_demand) / no_promo_demand * 100

top_category   = df.groupby("Category")["Revenue"].sum().idxmax()
top_region     = df.groupby("Region")["Demand"].sum().idxmax()
best_season    = df.groupby("Seasonality")["Demand"].mean().idxmax()
worst_season   = df.groupby("Seasonality")["Demand"].mean().idxmin()
pct_undercut   = (df["Price"] < df["Competitor Pricing"]).mean() * 100
zero_orders    = (df["Units Ordered"] == 0).mean() * 100

cat_revenue = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
region_units = df.groupby("Region")["Demand"].sum().sort_values(ascending=False)

# 3. BUILD SUMMARY STRING
summary = f"""
Dataset Overview:
- Rows: {total_rows:,}
- Date range: {date_min} to {date_max}
- Stores: {n_stores}, Products: {n_products}, Categories: {n_categories}

Demand & Revenue:
- Total units sold: {total_units:,}
- Total revenue: ${total_revenue:,.0f}
- Average unit price: ${avg_price:.2f}
- Average demand per row: {avg_demand:.1f} units

Promotion Effect:
- Avg demand WITHOUT promotion: {no_promo_demand:.1f} units
- Avg demand WITH promotion: {promo_demand:.1f} units
- Promotion uplift: +{promo_lift_pct:.1f}%

Category Revenue Ranking:
{cat_revenue.apply(lambda x: f"${x:,.0f}").to_string()}

Regional Demand Ranking:
{region_units.to_string()}

Seasonal Demand:
- Best season: {best_season}
- Weakest season: {worst_season}

Pricing Intelligence:
- Rows where our price is BELOW competitor: {pct_undercut:.1f}%
- Rows with zero units ordered: {zero_orders:.1f}%
"""

#  4. PRINT SUMMARY
print("=" * 65)
print("  PANDAS SUMMARY (sent to AI API)")
print("=" * 65)
print(summary)

#  5. CALL AI API
print("=" * 65)
print("  CALLING AI API …")
print("=" * 65)

prompt  = f"""
You are a business analyst writing for a retail executive.
Based on the dataset statistics below, write a single,
well-structured plain-English paragraph (5–7 sentences) that:
1. Summarises overall sales performance
2. Highlights the most important insight about promotions
3. Calls out which category and region are leading
4. Flags one data quality or pricing concern worth watching

Write confidently, no bullet points, no jargon. Just one clear paragraph.

Dataset Statistics:
{summary}
"""

try:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL,
        temperature=0.0,
        max_tokens=500,
    )
    ai_paragraph = chat_completion.choices[0].message.content.strip()
except Exception as e:
    print(f"An error occurred during Groq API call: {e}")
    ai_paragraph = "[API Error: An unexpected error occurred with Groq. Check your API key and network.]"

print("\n  AI-GENERATED PLAIN-ENGLISH INSIGHT")
print("-" * 65)
print()

import textwrap
for line in textwrap.wrap(ai_paragraph, width=65):
    print(f"  {line}")
print()
print("=" * 65)
print("  Done — summary computed by Pandas, paragraph by Groq API.")
print("=" * 65)
print()
