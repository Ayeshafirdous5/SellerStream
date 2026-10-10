import pandas as pd

input_path = "data/processed/orders_processed.csv"

df = pd.read_csv(input_path)
df["order_date"] = pd.to_datetime(df["order_date"])

print("Processed data loaded successfully!")
print("Number of rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())
print("\nCreating business-ready columns...")

df["net_revenue"] = df["total_amount"]

df["is_completed_order"] = (
    df["order_status"] == "Delivered"
).astype(int)

df["is_cancelled_order"] = (
    df["order_status"] == "Cancelled"
).astype(int)

df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

print("Business columns created!")

print(df[[
    "order_id",
    "net_revenue",
    "is_completed_order",
    "is_cancelled_order",
    "order_month"
]].head())
from pathlib import Path

output_path = "data/curated/orders_curated.csv"
Path("data/curated").mkdir(parents=True, exist_ok=True)

if Path(output_path).exists():
    existing_df = pd.read_csv(output_path)

    combined_df = pd.concat(
        [existing_df, df],
        ignore_index=True
    )

    combined_df = combined_df.drop_duplicates(
        subset=["order_id"],
        keep="last"
    )

    df = combined_df

    print("Existing curated data loaded.")
else:
    print("No existing curated data found. Initial load.")

df.to_csv(output_path, index=False)

print("\nIncremental curated data saved successfully!")
print("Total unique orders:", df["order_id"].nunique())
print("Output:", output_path)