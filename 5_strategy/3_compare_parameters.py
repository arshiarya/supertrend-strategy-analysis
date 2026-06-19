import pandas as pd

# -------------------------------
# LOAD FILES
# -------------------------------
df_7_1 = pd.read_csv("../data/securities/final_summary_7_1.csv")
df_10_2 = pd.read_csv("../data/securities/final_summary_10_2.csv")

# -------------------------------
# BASIC COMPARISON
# -------------------------------
print("\n📊 AVERAGE PERFORMANCE")

print("\n7,1 Average Annual Return:", df_7_1["Annual_Return"].mean())
print("10,2 Average Annual Return:", df_10_2["Annual_Return"].mean())

print("\n7,1 Average Accuracy:", df_7_1["Accuracy"].mean())
print("10,2 Average Accuracy:", df_10_2["Accuracy"].mean())

# -------------------------------
# CATEGORY DISTRIBUTION
# -------------------------------
print("\n📊 CATEGORY DISTRIBUTION")

print("\n7,1:\n", df_7_1["Category"].value_counts())
print("\n10,2:\n", df_10_2["Category"].value_counts())

# -------------------------------
# STOCK LEVEL COMPARISON
# -------------------------------
merged = df_7_1.merge(df_10_2, on="Symbol", suffixes=("_7_1", "_10_2"))

print("\n📊 SAMPLE STOCK COMPARISON")
print(merged[[
    "Symbol",
    "Annual_Return_7_1",
    "Annual_Return_10_2",
    "Accuracy_7_1",
    "Accuracy_10_2"
]].head(10))

# -------------------------------
# WHICH PARAMETER IS BETTER?
# -------------------------------
better_return = (merged["Annual_Return_10_2"] > merged["Annual_Return_7_1"]).sum()
better_accuracy = (merged["Accuracy_10_2"] > merged["Accuracy_7_1"]).sum()

print("\n📊 FINAL RESULT")
print(f"10,2 better in return for {better_return} stocks")
print(f"10,2 better in accuracy for {better_accuracy} stocks")