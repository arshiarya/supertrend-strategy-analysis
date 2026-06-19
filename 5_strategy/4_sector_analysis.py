import pandas as pd

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("../data/securities/final_summary_10_2.csv")
sector_map = pd.read_csv("../data/securities/nifty500.csv")

# -------------------------------
# MERGE
# -------------------------------
merged = df.merge(sector_map, on="Symbol")

# -------------------------------
# GROUP BY INDUSTRY
# -------------------------------
sector_analysis = merged.groupby("Industry").agg({
    "Annual_Return": "mean",
    "Accuracy": "mean",
    "Symbol": "count"
}).rename(columns={"Symbol": "Stock_Count"})

# -------------------------------
# SORT BEST TO WORST
# -------------------------------
sector_analysis = sector_analysis.sort_values(by="Annual_Return", ascending=False)

print("\n📊 INDUSTRY PERFORMANCE:\n")
print(sector_analysis)

# -------------------------------
# CATEGORY ANALYSIS
# -------------------------------
category_sector = merged.groupby(["Industry", "Category"]).size().unstack(fill_value=0)

print("\n📊 CATEGORY BY INDUSTRY:\n")
print(category_sector)