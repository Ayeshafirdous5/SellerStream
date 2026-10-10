import pandas as pd

file_path = "data/raw/orders_raw.csv"

df = pd.read_csv(file_path)

from pathlib import Path

Path("data/processed").mkdir(parents=True, exist_ok=True)
Path("data/rejected").mkdir(parents=True, exist_ok=True)

df["order_date"] = pd.to_datetime(df["order_date"])

print("Raw data loaded successfully!")
print("Number of rows:", len(df))
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())

missing_rows = df[df.isnull().any(axis=1)].copy()
print("Rows with missing values:", len(missing_rows))

if not missing_rows.empty:
    rejected_path = "data/rejected/missing_values.csv"
    missing_rows.to_csv(rejected_path, index=False)
    print("Rows with missing values saved to:", rejected_path)

    df = df.dropna().copy()
else:
    print("No rows with missing values to reject.")
print("\nNumeric validation:")

invalid_numeric = df[
    (df["quantity"] <= 0)
    | (df["unit_price"] <= 0)
    | (df["discount_amount"] < 0)
    | (df["total_amount"] < 0)
].copy()

print("Invalid numeric rows:", len(invalid_numeric))

if not invalid_numeric.empty:
    rejected_path = "data/rejected/invalid_numeric.csv"
    invalid_numeric.to_csv(rejected_path, index=False)
    print("Invalid numeric rows saved to:", rejected_path)

    df = df.drop(index=invalid_numeric.index).copy()
else:
    print("No invalid numeric rows found.")
print("\nDuplicate validation:")

duplicate_orders = df["order_id"].duplicated().sum()

print("Duplicate order IDs:", duplicate_orders)
duplicate_rows = df[df["order_id"].duplicated(keep=False)].copy()

print("Rows affected by duplicates:", len(duplicate_rows))

if not duplicate_rows.empty:
    rejected_path = "data/rejected/duplicate_orders.csv"
    duplicate_rows.to_csv(rejected_path, index=False)
    print("Duplicate rows saved to:", rejected_path)

    df = df.drop_duplicates(subset=["order_id"], keep=False).copy()
else:
    print("No duplicate rows to reject.")
print("\nAmount consistency validation:")

calculated_amount = (
    df["quantity"] * df["unit_price"]
    - df["discount_amount"]
)

mismatch_mask = df["total_amount"] != calculated_amount
mismatch_rows = df[mismatch_mask].copy()

print("Amount mismatches:", len(mismatch_rows))

if not mismatch_rows.empty:
    rejected_path = "data/rejected/amount_mismatches.csv"
    mismatch_rows.to_csv(rejected_path, index=False)
    print("Mismatched rows saved to:", rejected_path)

    df = df.loc[~mismatch_mask].copy()
else:
    print("No amount mismatches found.")
print("\nStatus validation:")

allowed_statuses = {"Delivered", "Shipped", "Cancelled"}

invalid_status_mask = ~df["order_status"].isin(allowed_statuses)
invalid_status_rows = df[invalid_status_mask].copy()

print("Invalid status rows:", len(invalid_status_rows))

if not invalid_status_rows.empty:
    rejected_path = "data/rejected/invalid_statuses.csv"
    invalid_status_rows.to_csv(rejected_path, index=False)
    print("Invalid status rows saved to:", rejected_path)

    df = df.loc[~invalid_status_mask].copy()
else:
    print("No invalid statuses found.")

print("\nData transformation:")

df["gross_amount"] = df["quantity"] * df["unit_price"]

df["discount_percentage"] = (
    df["discount_amount"] / df["gross_amount"] * 100
).round(2)

df["order_status"] = df["order_status"].str.strip().str.title()
print("\nStandardized order statuses:")
print(df["order_status"].unique())

print("Gross amount column created!")
print(df[[
    "order_id",
    "gross_amount",
    "discount_amount",
    "discount_percentage",
    "total_amount"
]].head())

output_path = "data/processed/orders_processed.csv"

df.to_csv(output_path, index=False)

print("\nProcessed data saved successfully!")
print("Output:", output_path)