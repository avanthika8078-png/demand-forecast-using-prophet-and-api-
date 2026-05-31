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
import numpy as np

# DATA = "/mnt/user-data/uploads/demand_forecasting_2.csv"
DATA = f"{path}/demand_forecasting.csv" 
#  1. LOAD
df = pd.read_csv(DATA, parse_dates=["Date"])

products = (df.groupby(["Product ID", "Category"])
              .agg(
                  store_count    = ("Store ID",          "nunique"),
                  avg_price      = ("Price",             "mean"),
                  min_price      = ("Price",             "min"),
                  avg_competitor = ("Competitor Pricing","mean"),
                  total_demand   = ("Demand",            "sum"),
                  avg_discount   = ("Discount",          "mean"),
              )
              .reset_index())
products.rename(columns={"Product ID": "sku", "Category": "category",
                          "avg_price": "unit_price",
                          "avg_competitor": "competitor_price"}, inplace=True)

# Inject dirty data for demonstration of all 5 checks
import numpy as np
rng = np.random.default_rng(42)
# Missing description column (realistic — not in original CSV)
products["description"] = [f"Description for {s}" for s in products["sku"]]
blank_idx = rng.choice(len(products), 3, replace=False)
products.loc[blank_idx, "description"] = ""

# Cost column (competitor price used as a cost proxy)
products["cost_price"] = products["competitor_price"]
# Force 3 products where cost exceeds our price
over_idx = rng.choice(len(products), 3, replace=False)
products.loc[over_idx, "cost_price"] = products.loc[over_idx, "unit_price"] * rng.uniform(1.1, 1.6, 3)

# Force 2 zero/negative prices
bad_price_idx = rng.choice(len(products), 2, replace=False)
products.loc[bad_price_idx[0], "unit_price"] = 0
products.loc[bad_price_idx[1], "unit_price"] = -5.0

# Force 2 missing categories
no_cat_idx = rng.choice(len(products), 2, replace=False)
products.loc[no_cat_idx, "category"] = ""

# Force 2 duplicate SKUs
dup_idx = rng.choice(len(products), 2, replace=False)
products.loc[dup_idx, "sku"] = products.iloc[0]["sku"]

# 2. RUN CHECKS
issues = {}

# Check 1 – Missing product descriptions
mask1 = products["description"].isna() | (products["description"].str.strip() == "")
issues["missing_description"] = products[mask1][["sku", "category"]].copy()

# Check 2 – Zero or negative unit prices
products["unit_price"] = pd.to_numeric(products["unit_price"], errors="coerce")
mask2 = products["unit_price"].isna() | (products["unit_price"] <= 0)
issues["invalid_unit_price"] = products[mask2][["sku", "category", "unit_price"]].copy()

# Check 3 – Cost exceeds selling price
products["cost_price"] = pd.to_numeric(products["cost_price"], errors="coerce")
mask3 = products["cost_price"] > products["unit_price"]
issues["cost_exceeds_price"] = products[mask3][["sku", "category", "unit_price", "cost_price"]].copy()
issues["cost_exceeds_price"]["loss_per_unit"] = (
    issues["cost_exceeds_price"]["cost_price"] - issues["cost_exceeds_price"]["unit_price"]
).round(2)

# Check 4 – No category assigned
mask4 = products["category"].isna() | (products["category"].str.strip() == "")
issues["missing_category"] = products[mask4][["sku", "unit_price"]].copy()

# Check 5 – Duplicate SKUs
dup_mask = products.duplicated(subset=["sku"], keep=False)
issues["duplicate_skus"] = products[dup_mask][["sku", "category", "unit_price"]].sort_values("sku").copy()

# 3. ALSO CHECK RAW DATASET
raw_issues = {}
raw_issues["zero_demand_rows"]      = int((df["Demand"] <= 0).sum())
raw_issues["zero_price_rows"]       = int((df["Price"] <= 0).sum())
raw_issues["negative_inventory"]    = int((df["Inventory Level"] < 0).sum())
raw_issues["units_ordered_zero"]    = int((df["Units Ordered"] == 0).sum())
raw_issues["price_below_competitor"]= int((df["Price"] < df["Competitor Pricing"]).sum())

# 4. PRINT REPORT
SEP  = "=" * 65
SEP2 = "-" * 65
total_product_issues = sum(len(v) for v in issues.values())

def fmt_table(d, max_rows=12):
    if d.empty:
        return "  (none)"
    rows = d.head(max_rows).to_string(index=False)
    lines = ["  " + l for l in rows.splitlines()]
    if len(d) > max_rows:
        lines.append(f"  … and {len(d) - max_rows} more")
    return "\n".join(lines)

print()
print(SEP)
print("     PRODUCT DATABASE — DATA QUALITY REPORT")
print("     Source: demand_forecasting.csv")
print(SEP)
print(f"  Raw rows in dataset        : {len(df):,}")
print(f"  Unique products (SKUs)     : {df['Product ID'].nunique()}")
print(f"  Stores covered             : {df['Store ID'].nunique()}")
print(f"  Date range                 : {df['Date'].min().date()} → {df['Date'].max().date()}")
print(SEP)

print(f"\n[1] MISSING PRODUCT DESCRIPTIONS — {len(issues['missing_description'])} product(s)")
print(SEP2)
print(fmt_table(issues["missing_description"]))

print(f"\n[2] ZERO OR NEGATIVE UNIT PRICES — {len(issues['invalid_unit_price'])} product(s)")
print(SEP2)
print(fmt_table(issues["invalid_unit_price"]))

print(f"\n[3] COST EXCEEDS SELLING PRICE — {len(issues['cost_exceeds_price'])} product(s)")
print(SEP2)
print(fmt_table(issues["cost_exceeds_price"]))

print(f"\n[4] NO CATEGORY ASSIGNED — {len(issues['missing_category'])} product(s)")
print(SEP2)
print(fmt_table(issues["missing_category"]))

print(f"\n[5] DUPLICATE SKUs — {len(issues['duplicate_skus'])} rows "
      f"({issues['duplicate_skus']['sku'].nunique() if not issues['duplicate_skus'].empty else 0} duplicated SKU(s))")
print(SEP2)
print(fmt_table(issues["duplicate_skus"]))

print(f"\n{SEP}")
print("  RAW DATASET CHECKS (all 76,000 rows)")
print(SEP2)
for label, count in raw_issues.items():
    flag = "✗" if count else "✓"
    print(f"  {flag}  {label.replace('_',' '):<32} {count:>6,} row(s)")

print(f"\n{SEP}")
print("  PRODUCT-LEVEL ISSUE SCORECARD")
print(SEP2)
scorecard = {
    "Missing descriptions"    : len(issues["missing_description"]),
    "Invalid unit prices"      : len(issues["invalid_unit_price"]),
    "Cost > selling price"     : len(issues["cost_exceeds_price"]),
    "Missing categories"       : len(issues["missing_category"]),
    "Duplicate SKU rows"       : len(issues["duplicate_skus"]),
}
for label, count in scorecard.items():
    flag   = "✗" if count else "✓"
    status = f"{count:>4} issue(s)" if count else "  No issues"
    print(f"  {flag}  {label:<30} {status}")

score = max(0, 100 - (total_product_issues * 5))
print(SEP2)
print(f"  Data quality score : {score:.0f} / 100  "
      f"({'PASS ✓' if total_product_issues == 0 else 'NEEDS ATTENTION ⚠'})")
print(SEP)
print()
