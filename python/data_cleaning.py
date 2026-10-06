import os
import pandas as pd


# ============================================================
# CUSTOMER CHURN ANALYTICS
# DATA CLEANING
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

os.makedirs(
    PROCESSED_DIR,
    exist_ok=True
)


print("=" * 70)
print("CUSTOMER CHURN DATA CLEANING")
print("=" * 70)


# ============================================================
# 1. LOAD RAW DATA
# ============================================================

customers = pd.read_csv(
    os.path.join(RAW_DIR, "customers.csv"),
    parse_dates=["Join_Date"]
)

subscriptions = pd.read_csv(
    os.path.join(RAW_DIR, "subscriptions.csv")
)

usage = pd.read_csv(
    os.path.join(RAW_DIR, "usage.csv")
)

customer_status = pd.read_csv(
    os.path.join(RAW_DIR, "customer_status.csv"),
    parse_dates=["Churn_Date"]
)


# ============================================================
# 2. INITIAL COUNTS
# ============================================================

print("\nInitial row counts:")

print(f"Customers       : {len(customers):,}")
print(f"Subscriptions   : {len(subscriptions):,}")
print(f"Usage           : {len(usage):,}")
print(f"Customer Status : {len(customer_status):,}")


# ============================================================
# 3. REMOVE DUPLICATES
# ============================================================

print("\n" + "=" * 70)
print("REMOVING DUPLICATES")
print("=" * 70)


before = len(customers)

customers = customers.drop_duplicates(
    subset=["Customer_ID"]
)

print(
    f"Customers duplicates removed: "
    f"{before - len(customers):,}"
)


before = len(subscriptions)

subscriptions = subscriptions.drop_duplicates(
    subset=["Customer_ID"]
)

print(
    f"Subscription duplicates removed: "
    f"{before - len(subscriptions):,}"
)


before = len(usage)

usage = usage.drop_duplicates(
    subset=["Customer_ID"]
)

print(
    f"Usage duplicates removed: "
    f"{before - len(usage):,}"
)


before = len(customer_status)

customer_status = customer_status.drop_duplicates(
    subset=["Customer_ID"]
)

print(
    f"Status duplicates removed: "
    f"{before - len(customer_status):,}"
)


# ============================================================
# 4. HANDLE MISSING SUPPORT TICKETS
# ============================================================

print("\n" + "=" * 70)
print("CLEANING SUPPORT TICKETS")
print("=" * 70)

missing_support = (
    usage["Support_Tickets"]
    .isna()
    .sum()
)

support_median = (
    usage["Support_Tickets"]
    .median()
)

print(
    f"Missing values: {missing_support:,}"
)

print(
    f"Median Support Tickets: "
    f"{support_median}"
)

usage["Support_Tickets"] = (
    usage["Support_Tickets"]
    .fillna(support_median)
)


# Convert back to integer
usage["Support_Tickets"] = (
    usage["Support_Tickets"]
    .round()
    .astype(int)
)

print(
    f"Remaining missing values: "
    f"{usage['Support_Tickets'].isna().sum():,}"
)


# ============================================================
# 5. HANDLE MISSING SATISFACTION
# ============================================================

print("\n" + "=" * 70)
print("CLEANING SATISFACTION SCORE")
print("=" * 70)

missing_satisfaction = (
    customer_status["Satisfaction_Score"]
    .isna()
    .sum()
)

satisfaction_median = (
    customer_status["Satisfaction_Score"]
    .median()
)

print(
    f"Missing values: "
    f"{missing_satisfaction:,}"
)

print(
    f"Median Satisfaction Score: "
    f"{satisfaction_median}"
)

customer_status[
    "Satisfaction_Score"
] = (
    customer_status[
        "Satisfaction_Score"
    ]
    .fillna(satisfaction_median)
)

customer_status[
    "Satisfaction_Score"
] = (
    customer_status[
        "Satisfaction_Score"
    ]
    .round()
    .astype(int)
)

print(
    f"Remaining missing values: "
    f"{customer_status['Satisfaction_Score'].isna().sum():,}"
)


# ============================================================
# 6. DATA TYPE STANDARDIZATION
# ============================================================

print("\n" + "=" * 70)
print("STANDARDIZING DATA TYPES")
print("=" * 70)


customers["Customer_ID"] = (
    customers["Customer_ID"]
    .astype(str)
)

subscriptions["Customer_ID"] = (
    subscriptions["Customer_ID"]
    .astype(str)
)

usage["Customer_ID"] = (
    usage["Customer_ID"]
    .astype(str)
)

customer_status["Customer_ID"] = (
    customer_status["Customer_ID"]
    .astype(str)
)


# ============================================================
# 7. VALIDATE CUSTOMER RELATIONSHIPS
# ============================================================

print("\n" + "=" * 70)
print("VALIDATING RELATIONSHIPS")
print("=" * 70)

customer_ids = set(
    customers["Customer_ID"]
)

subscription_ids = set(
    subscriptions["Customer_ID"]
)

usage_ids = set(
    usage["Customer_ID"]
)

status_ids = set(
    customer_status["Customer_ID"]
)


print(
    "Subscription IDs missing from Customers:",
    len(subscription_ids - customer_ids)
)

print(
    "Usage IDs missing from Customers:",
    len(usage_ids - customer_ids)
)

print(
    "Status IDs missing from Customers:",
    len(status_ids - customer_ids)
)


# ============================================================
# 8. VALIDATE CHURN LOGIC
# ============================================================

print("\n" + "=" * 70)
print("VALIDATING CHURN LOGIC")
print("=" * 70)


# Active customers should not have churn dates
invalid_active_dates = (
    customer_status.loc[
        customer_status["Churn"] == "No",
        "Churn_Date"
    ]
    .notna()
    .sum()
)

print(
    "Active customers with churn dates:",
    invalid_active_dates
)


# Churned customers should have churn reasons
invalid_churn_reasons = (
    customer_status.loc[
        customer_status["Churn"] == "Yes",
        "Churn_Reason"
    ]
    .isna()
    .sum()
)

print(
    "Churned customers without reasons:",
    invalid_churn_reasons
)


# ============================================================
# 9. SAVE PROCESSED DATA
# ============================================================

print("\n" + "=" * 70)
print("SAVING PROCESSED DATA")
print("=" * 70)


customers.to_csv(
    os.path.join(
        PROCESSED_DIR,
        "customers_clean.csv"
    ),
    index=False
)

subscriptions.to_csv(
    os.path.join(
        PROCESSED_DIR,
        "subscriptions_clean.csv"
    ),
    index=False
)

usage.to_csv(
    os.path.join(
        PROCESSED_DIR,
        "usage_clean.csv"
    ),
    index=False
)

customer_status.to_csv(
    os.path.join(
        PROCESSED_DIR,
        "customer_status_clean.csv"
    ),
    index=False
)


# ============================================================
# 10. FINAL QUALITY CHECK
# ============================================================

print("\n" + "=" * 70)
print("FINAL QUALITY CHECK")
print("=" * 70)


tables = {
    "Customers": customers,
    "Subscriptions": subscriptions,
    "Usage": usage,
    "Customer Status": customer_status
}

for name, df in tables.items():

    print(
        f"{name:<20} "
        f"Rows: {len(df):>10,} | "
        f"Missing Values: {df.isna().sum().sum():>6,}"
    )


print("\nFiles saved to:")

print(PROCESSED_DIR)

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETE")
print("=" * 70)