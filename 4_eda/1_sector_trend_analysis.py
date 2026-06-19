# This code analyzes sector trends by loading sector return data, selecting the top 5 sectors based on average returns, and plotting their cumulative growth over time. The cumulative returns are calculated to show the growth of each sector from a base value of 1, allowing for a clear comparison of their performance over time.
# import pandas as pd
# import matplotlib.pyplot as plt

# # STEP 1: Load sector returns
# df = pd.read_csv("../data/securities/sector_returns.csv")

# # STEP 2: Convert date
# df["Date"] = pd.to_datetime(df["Date"])

# # STEP 3: Pivot data (VERY IMPORTANT)
# top_sectors = df.groupby("Sector")["Sector_Return"].mean().nlargest(5).index
# filtered = df[df["Sector"].isin(top_sectors)]

# pivot_df = filtered.pivot(index="Date", columns="Sector", values="Sector_Return")

# # STEP 4: Plot
# plt.figure(figsize=(14,7))
# for sector in pivot_df.columns:
#     smoothed = pivot_df[sector].rolling(window=4).mean()
#     plt.plot(pivot_df.index, smoothed, label=sector)
# plt.title("Sector Performance Over Time")
# plt.xlabel("Date")
# plt.ylabel("Weekly Return")
# plt.legend()
# plt.grid()

# plt.show()


# cummulative returns are more intuitive for growth comparison, but we can also plot raw returns with smoothing to see trends without compounding effects.
# import pandas as pd
# import matplotlib.pyplot as plt

# # STEP 1: Load sector returns
# df = pd.read_csv("../data/securities/sector_returns.csv")

# # STEP 2: Convert Date column
# df["Date"] = pd.to_datetime(df["Date"])

# # STEP 3: Select top 5 sectors (based on average return)
# top_sectors = df.groupby("Sector")["Sector_Return"].mean().nlargest(5).index
# df = df[df["Sector"].isin(top_sectors)]

# # STEP 4: Pivot data
# pivot_df = df.pivot(index="Date", columns="Sector", values="Sector_Return")

# # STEP 5: Convert to cumulative returns (IMPORTANT FIX)
# cum_df = (1 + pivot_df).cumprod()

# # STEP 6: Plot
# plt.figure(figsize=(14,7))

# for sector in cum_df.columns:
#     plt.plot(cum_df.index, cum_df[sector], label=sector)

# plt.title("Sector Growth Over Time (Cumulative Returns)")
# plt.xlabel("Date")
# plt.ylabel("Growth (Base = 1)")
# plt.legend()
# plt.grid()

# plt.show()


# montly returns with date from 2019 onwards, and cumulative growth for better visualization of trends.
import pandas as pd
import matplotlib.pyplot as plt

# STEP 1: Load data
df = pd.read_csv("../data/securities/sector_returns.csv")

# STEP 2: Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# STEP 3: Filter recent years (optional but recommended)
df = df[df["Date"] >= "2019-01-01"]

# STEP 4: Convert weekly → monthly
df["Month"] = df["Date"].dt.to_period("M")

monthly_df = df.groupby(["Month", "Sector"])["Sector_Return"].mean().reset_index()
monthly_df["Month"] = monthly_df["Month"].dt.to_timestamp()

# STEP 5: Select top 5 sectors
top_sectors = monthly_df.groupby("Sector")["Sector_Return"].mean().nlargest(5).index
monthly_df = monthly_df[monthly_df["Sector"].isin(top_sectors)]

# STEP 6: Pivot
pivot_df = monthly_df.pivot(index="Month", columns="Sector", values="Sector_Return")

# STEP 7: Cumulative returns
cum_df = (1 + pivot_df).cumprod()

# STEP 8: Plot
plt.figure(figsize=(14,7))

for sector in cum_df.columns:
    plt.plot(cum_df.index, cum_df[sector], label=sector)

plt.title("Sector Growth Over Time (Monthly, Cumulative)")
plt.xlabel("Date")
plt.ylabel("Growth (Base = 1)")
plt.legend()
plt.grid()

plt.show()