import pandas as pd
import sys

input_path = "data/curated/orders_curated.csv"

df = pd.read_csv(input_path)

print("Curated data loaded successfully!")
print("Number of rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())
print("\nRequired field validation:")

required_columns = [
    "order_id",
    "customer_id",
    "product_id",
    "seller_id",
    "order_date",
    "quantity",
    "unit_price",
    "total_amount",
    "order_status"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

print("Missing required columns:", missing_columns)

if len(missing_columns) == 0:
    print("Required field validation passed!")
else:
    print("Required field validation failed!")
print("\nDuplicate validation:")

duplicate_orders = df["order_id"].duplicated().sum()

print("Duplicate order IDs:", duplicate_orders)

if duplicate_orders == 0:
    print("Duplicate validation passed!")
else:
    print("Duplicate validation failed!")
print("\nNumeric validation:")

invalid_quantity = (df["quantity"] <= 0).sum()
invalid_unit_price = (df["unit_price"] <= 0).sum()
invalid_total_amount = (df["total_amount"] < 0).sum()
invalid_discount = (df["discount_amount"] < 0).sum()

print("Invalid quantity:", invalid_quantity)
print("Invalid unit price:", invalid_unit_price)
print("Invalid total amount:", invalid_total_amount)
print("Invalid discount amount:", invalid_discount)

if (
    invalid_quantity == 0
    and invalid_unit_price == 0
    and invalid_total_amount == 0
    and invalid_discount == 0
):
    print("Numeric validation passed!")
else:
    print("Numeric validation failed!")
print("\nAmount consistency validation:")

calculated_amount = (
    df["quantity"] * df["unit_price"]
    - df["discount_amount"]
)

amount_mismatches = (
    df["total_amount"] != calculated_amount
).sum()

print("Amount mismatches:", amount_mismatches)

if amount_mismatches == 0:
    print("Amount consistency validation passed!")
else:
    print("Amount consistency validation failed!")
print("\nStatus validation:")

allowed_statuses = {
    "Delivered",
    "Shipped",
    "Cancelled"
}

invalid_statuses = df.loc[
    ~df["order_status"].isin(allowed_statuses),
    "order_status"
].unique()

print("Invalid statuses:", invalid_statuses)

if len(invalid_statuses) == 0:
    print("Status validation passed!")
else:
    print("Status validation failed!")
print("\nDate validation:")

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

invalid_dates = df["order_date"].isna().sum()

future_dates = (
    df["order_date"] > pd.Timestamp.today()
).sum()

print("Invalid dates:", invalid_dates)
print("Future dates:", future_dates)

if invalid_dates == 0 and future_dates == 0:
    print("Date validation passed!")
else:
    print("Date validation failed!")

validation_passed = (
    len(missing_columns) == 0
    and duplicate_orders == 0
    and invalid_quantity == 0
    and invalid_unit_price == 0
    and invalid_total_amount == 0
    and invalid_discount == 0
    and amount_mismatches == 0
    and len(invalid_statuses) == 0
    and invalid_dates == 0
    and future_dates == 0
)

print("\n" + "=" * 45)
print("DATA QUALITY VALIDATION SUMMARY")
print("=" * 45)

if validation_passed:
    print("Overall data quality status: PASS")
else:
    print("Overall data quality status: FAIL")

print("=" * 45)
if not validation_passed:
    sys.exit(1)