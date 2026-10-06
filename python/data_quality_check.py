import os
import pandas as pd

# ============================================================
# CUSTOMER CHURN ANALYTICS
# DATA QUALITY AUDIT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)


# ============================================================
# 1. LOAD DATA
# ============================================================

print("=" * 70)
print("CUSTOMER CHURN DATA QUALITY AUDIT")
print("=" * 70)

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


tables = {
    "Customers": customers,
    "Subscriptions": subscriptions,
    "Usage": usage,
    "Customer Status": customer_status
}


# ============================================================
# 2. BASIC TABLE INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("1. TABLE DIMENSIONS")
print("=" * 70)

for name, df in tables.items():

    print(
        f"{name:<20} "
        f"Rows: {len(df):>10,} | "
        f"Columns: {len(df.columns):>3}"
    )


# ============================================================
# 3. COLUMN INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("2. COLUMN INFORMATION")
print("=" * 70)

for name, df in tables.items():

    print(f"\n--- {name} ---")

    for column in df.columns:

        print(
            f"{column:<30} "
            f"{str(df[column].dtype):<15} "
            f"Unique: {df[column].nunique(dropna=True):>10,}"
        )


# ============================================================
# 4. MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("3. MISSING VALUES")
print("=" * 70)

for name, df in tables.items():

    print(f"\n--- {name} ---")

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if len(missing) == 0:

        print("No missing values.")

    else:

        for column, count in missing.items():

            percentage = (
                count / len(df)
            ) * 100

            print(
                f"{column:<30} "
                f"{count:>8,} "
                f"({percentage:.3f}%)"
            )


# ============================================================
# 5. DUPLICATE ROWS
# ============================================================

print("\n" + "=" * 70)
print("4. DUPLICATE ROWS")
print("=" * 70)

for name, df in tables.items():

    duplicates = df.duplicated().sum()

    print(
        f"{name:<20}: {duplicates:,} duplicate rows"
    )


# ============================================================
# 6. DUPLICATE CUSTOMER IDs
# ============================================================

print("\n" + "=" * 70)
print("5. DUPLICATE CUSTOMER IDs")
print("=" * 70)

for name, df in tables.items():

    if "Customer_ID" in df.columns:

        duplicate_ids = (
            df["Customer_ID"].duplicated().sum()
        )

        print(
            f"{name:<20}: "
            f"{duplicate_ids:,} duplicate Customer_IDs"
        )


# ============================================================
# 7. CUSTOMER ID CONSISTENCY
# ============================================================

print("\n" + "=" * 70)
print("6. CUSTOMER ID REFERENTIAL INTEGRITY")
print("=" * 70)

master_ids = set(
    customers["Customer_ID"]
)

for name, df in tables.items():

    if name == "Customers":
        continue

    ids = set(
        df["Customer_ID"]
    )

    missing_from_master = (
        ids - master_ids
    )

    print(
        f"{name:<20}: "
        f"{len(missing_from_master):,} IDs "
        f"not found in Customers"
    )


# ============================================================
# 8. RANGE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("7. RANGE VALIDATION")
print("=" * 70)


# Age
invalid_age = (
    (customers["Age"] < 18)
    |
    (customers["Age"] > 70)
).sum()

print(
    f"Invalid Age values: "
    f"{invalid_age:,}"
)


# Tenure
invalid_tenure = (
    (customers["Tenure_Months"] < 1)
    |
    (customers["Tenure_Months"] > 44)
).sum()

print(
    f"Invalid Tenure values: "
    f"{invalid_tenure:,}"
)


# Monthly charges
invalid_charges = (
    (subscriptions["Monthly_Charges"] < 0)
).sum()

print(
    f"Invalid Monthly Charges: "
    f"{invalid_charges:,}"
)


# Usage
invalid_usage = (
    (usage["Avg_Monthly_Usage_Hours"] < 0)
).sum()

print(
    f"Invalid Usage Hours: "
    f"{invalid_usage:,}"
)


# Satisfaction
invalid_satisfaction = (
    (
        customer_status["Satisfaction_Score"]
        < 1
    )
    |
    (
        customer_status["Satisfaction_Score"]
        > 10
    )
).sum()

print(
    f"Invalid Satisfaction Scores: "
    f"{invalid_satisfaction:,}"
)


# ============================================================
# 9. CATEGORICAL VALUES
# ============================================================

print("\n" + "=" * 70)
print("8. CATEGORICAL VALUE CHECK")
print("=" * 70)

print("\nPlans:")
print(
    subscriptions["Plan"]
    .value_counts()
)

print("\nContract Types:")
print(
    subscriptions["Contract_Type"]
    .value_counts()
)

print("\nPayment Methods:")
print(
    subscriptions["Payment_Method"]
    .value_counts()
)

print("\nChurn:")
print(
    customer_status["Churn"]
    .value_counts()
)

print("\nChurn Reasons:")
print(
    customer_status["Churn_Reason"]
    .value_counts(dropna=False)
)


# ============================================================
# 10. CHURN RATE
# ============================================================

print("\n" + "=" * 70)
print("9. CHURN METRICS")
print("=" * 70)

total_customers = len(
    customer_status
)

churned_customers = (
    customer_status["Churn"]
    .eq("Yes")
    .sum()
)

churn_rate = (
    churned_customers
    / total_customers
) * 100

print(
    f"Total Customers : {total_customers:,}"
)

print(
    f"Churned Customers: {churned_customers:,}"
)

print(
    f"Churn Rate       : {churn_rate:.2f}%"
)


# ============================================================
# 11. DATE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("10. DATE VALIDATION")
print("=" * 70)

invalid_join_dates = (
    customers["Join_Date"]
    > pd.Timestamp("2026-09-01")
).sum()

print(
    f"Future Join Dates: "
    f"{invalid_join_dates:,}"
)


# Churn dates for non-churned customers
invalid_non_churn_dates = (
    customer_status.loc[
        customer_status["Churn"] == "No",
        "Churn_Date"
    ]
    .notna()
    .sum()
)

print(
    f"Non-churned customers with Churn Date: "
    f"{invalid_non_churn_dates:,}"
)


# ============================================================
# 12. CHURN REASON CONSISTENCY
# ============================================================

print("\n" + "=" * 70)
print("11. CHURN REASON CONSISTENCY")
print("=" * 70)

churned_without_reason = (
    customer_status.loc[
        customer_status["Churn"] == "Yes",
        "Churn_Reason"
    ]
    .isna()
    .sum()
)

active_with_reason = (
    customer_status.loc[
        customer_status["Churn"] == "No",
        "Churn_Reason"
    ]
    .notna()
    .sum()
)

print(
    f"Churned customers without reason: "
    f"{churned_without_reason:,}"
)

print(
    f"Active customers with churn reason: "
    f"{active_with_reason:,}"
)


# ============================================================
# 13. REVENUE METRICS
# ============================================================

print("\n" + "=" * 70)
print("12. REVENUE CHECK")
print("=" * 70)

merged = (
    subscriptions[
        [
            "Customer_ID",
            "Monthly_Charges"
        ]
    ]
    .merge(
        customer_status[
            [
                "Customer_ID",
                "Churn"
            ]
        ],
        on="Customer_ID",
        how="inner"
    )
)

total_monthly_revenue = (
    merged["Monthly_Charges"]
    .sum()
)

churned_monthly_revenue = (
    merged.loc[
        merged["Churn"] == "Yes",
        "Monthly_Charges"
    ]
    .sum()
)

print(
    f"Total Monthly Revenue: "
    f"₹{total_monthly_revenue:,.2f}"
)

print(
    f"Monthly Revenue from Churned Customers: "
    f"₹{churned_monthly_revenue:,.2f}"
)


# ============================================================
# 14. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY AUDIT COMPLETE")
print("=" * 70)