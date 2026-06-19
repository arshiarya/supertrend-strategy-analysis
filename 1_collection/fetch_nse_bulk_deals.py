import os
import pandas as pd
from datetime import datetime
from nselib import capital_market

# ---- CONFIG ----
output_folder = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\data\\nse_bulk_deals"
# ----------------

os.makedirs(output_folder, exist_ok=True)

from_dt = "01-01-2001"
to_dt   = datetime.today().strftime("%d-%m-%Y")

data = capital_market.bulk_deal_data(from_date=from_dt, to_date=to_dt)
df   = pd.DataFrame(data)
filename = f"bulkdeals_{to_dt}.csv"
filepath = os.path.join(output_folder, filename)
df.to_csv(filepath, index=False)
print(f"NSE Bulk Deals saved: {len(df)} rows -> {filepath}")