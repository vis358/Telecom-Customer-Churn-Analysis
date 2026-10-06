import os
import pandas as pd
import numpy as np


# ============================================================
# CUSTOMER CHURN ANALYTICS
# EXPLORATORY DATA ANALYSIS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


print("=" * 70)
print("CUSTOMER CHURN EXPLORATORY DATA ANALYSIS")
print("=" * 70)


# ============================================================
# 1. LOAD DATA
# ============================================================

customers = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "customers_clean.csv"
    ),
    parse_dates=["Join_Date"]
)

subscriptions = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "subscriptions_clean.csv"
    )
)

usage = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "usage_clean.csv"
    )
)

status = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "customer_status_clean.csv"
    ),
    parse_dates=["Churn_Date"]
)


# ============================================================
# 2. CREATE ANALYTICAL DATASET
# ============================================================

df = (
    customers
    .merge(
        subscriptions,
        on="Customer_ID",
        how="inner"
    )
    .merge(
        usage,
        on="Customer_ID",
        how="inner"
    )
    .merge(
        status,
        on="Customer_ID",
        how="inner"
    )
)

print("\nCombined analytical dataset:")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 3. CORE KPIs
# ============================================================

print("\n" + "=" * 70)
print("1. CORE BUSINESS KPIs")
print("=" * 70)

total_customers = len(df)

churned_customers = (
    df["Churn"]
    .eq("Yes")
    .sum()
)

active_customers = (
    df["Churn"]
    .eq("No")
    .sum()
)

churn_rate = (
    churned_customers
    / total_customers
) * 100

total_monthly_revenue = (
    df["Monthly_Charges"]
    .sum()
)

churned_monthly_revenue = (
    df.loc[
        df["Churn"] == "Yes",
        "Monthly_Charges"
    ]
    .sum()
)

revenue_share_churned = (
    churned_monthly_revenue
    / total_monthly_revenue
) * 100

print(
    f"Total Customers       : {total_customers:,}"
)

print(
    f"Active Customers      : {active_customers:,}"
)

print(
    f"Churned Customers     : {churned_customers:,}"
)

print(
    f"Churn Rate            : {churn_rate:.2f}%"
)

print(
    f"Monthly Revenue       : ₹{total_monthly_revenue:,.2f}"
)

print(
    f"Churned Revenue       : ₹{churned_monthly_revenue:,.2f}"
)

print(
    f"Revenue Share Churned : {revenue_share_churned:.2f}%"
)


# ============================================================
# 4. CHURN BY CONTRACT
# ============================================================

print("\n" + "=" * 70)
print("2. CHURN BY CONTRACT TYPE")
print("=" * 70)

contract_analysis = (
    df.groupby("Contract_Type")
    .agg(
        Customers=("Customer_ID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        ),
        Monthly_Revenue=(
            "Monthly_Charges",
            "sum"
        )
    )
    .reset_index()
)

contract_analysis["Churn_Rate"] = (
    contract_analysis["Churned_Customers"]
    / contract_analysis["Customers"]
    * 100
)

contract_analysis = contract_analysis.sort_values(
    "Churn_Rate",
    ascending=False
)

print(
    contract_analysis.to_string(
        index=False
    )
)


# ============================================================
# 5. CHURN BY PLAN
# ============================================================

print("\n" + "=" * 70)
print("3. CHURN BY PLAN")
print("=" * 70)

plan_analysis = (
    df.groupby("Plan")
    .agg(
        Customers=("Customer_ID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        ),
        Monthly_Revenue=(
            "Monthly_Charges",
            "sum"
        )
    )
    .reset_index()
)

plan_analysis["Churn_Rate"] = (
    plan_analysis["Churned_Customers"]
    / plan_analysis["Customers"]
    * 100
)

plan_analysis = plan_analysis.sort_values(
    "Churn_Rate",
    ascending=False
)

print(
    plan_analysis.to_string(
        index=False
    )
)


# ============================================================
# 6. CHURN BY TENURE
# ============================================================

print("\n" + "=" * 70)
print("4. CHURN BY TENURE")
print("=" * 70)

df["Tenure_Group"] = pd.cut(
    df["Tenure_Months"],
    bins=[0, 6, 12, 24, 36, 100],
    labels=[
        "0-6 Months",
        "7-12 Months",
        "13-24 Months",
        "25-36 Months",
        "37+ Months"
    ]
)

tenure_analysis = (
    df.groupby(
        "Tenure_Group",
        observed=False
    )
    .agg(
        Customers=("Customer_ID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

tenure_analysis["Churn_Rate"] = (
    tenure_analysis["Churned_Customers"]
    / tenure_analysis["Customers"]
    * 100
)

print(
    tenure_analysis.to_string(
        index=False
    )
)


# ============================================================
# 7. CHURN BY SATISFACTION
# ============================================================

print("\n" + "=" * 70)
print("5. CHURN BY SATISFACTION")
print("=" * 70)

satisfaction_analysis = (
    df.groupby("Satisfaction_Score")
    .agg(
        Customers=("Customer_ID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

satisfaction_analysis["Churn_Rate"] = (
    satisfaction_analysis["Churned_Customers"]
    / satisfaction_analysis["Customers"]
    * 100
)

print(
    satisfaction_analysis.to_string(
        index=False
    )
)


# ============================================================
# 8. CHURN BY USAGE
# ============================================================

print("\n" + "=" * 70)
print("6. CHURN BY USAGE")
print("=" * 70)

df["Usage_Group"] = pd.cut(
    df["Avg_Monthly_Usage_Hours"],
    bins=[0, 10, 20, 40, 60, 100],
    labels=[
        "<10 Hours",
        "10-20 Hours",
        "20-40 Hours",
        "40-60 Hours",
        "60+ Hours"
    ]
)

usage_analysis = (
    df.groupby(
        "Usage_Group",
        observed=False
    )
    .agg(
        Customers=("Customer_ID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

usage_analysis["Churn_Rate"] = (
    usage_analysis["Churned_Customers"]
    / usage_analysis["Customers"]
    * 100
)

print(
    usage_analysis.to_string(
        index=False
    )
)


# ============================================================
# 9. CHURN BY SUPPORT TICKETS
# ============================================================

print("\n" + "=" * 70)
print("7. CHURN BY SUPPORT TICKETS")
print("=" * 70)

df["Support_Group"] = pd.cut(
    df["Support_Tickets"],
    bins=[-1, 1, 3, 5, 100],
    labels=[
        "0-1 Tickets",
        "2-3 Tickets",
        "4-5 Tickets",
        "6+ Tickets"
    ]
)

support_analysis = (
    df.groupby(
        "Support_Group",
        observed=False
    )
    .agg(
        Customers=("Customer_ID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

support_analysis["Churn_Rate"] = (
    support_analysis["Churned_Customers"]
    / support_analysis["Customers"]
    * 100
)

print(
    support_analysis.to_string(
        index=False
    )
)


# ============================================================
# 10. CHURN BY DOWNTIME
# ============================================================

print("\n" + "=" * 70)
print("8. CHURN BY DOWNTIME")
print("=" * 70)

df["Downtime_Group"] = pd.cut(
    df["Downtime_Hours"],
    bins=[-1, 2, 4, 7, 100],
    labels=[
        "0-2 Hours",
        "2-4 Hours",
        "4-7 Hours",
        "7+ Hours"
    ]
)

downtime_analysis = (
    df.groupby(
        "Downtime_Group",
        observed=False
    )
    .agg(
        Customers=("Customer_ID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

downtime_analysis["Churn_Rate"] = (
    downtime_analysis["Churned_Customers"]
    / downtime_analysis["Customers"]
    * 100
)

print(
    downtime_analysis.to_string(
        index=False
    )
)


# ============================================================
# 11. CHURN BY PAYMENT METHOD
# ============================================================

print("\n" + "=" * 70)
print("9. CHURN BY PAYMENT METHOD")
print("=" * 70)

payment_analysis = (
    df.groupby("Payment_Method")
    .agg(
        Customers=("Customer_ID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

payment_analysis["Churn_Rate"] = (
    payment_analysis["Churned_Customers"]
    / payment_analysis["Customers"]
    * 100
)

payment_analysis = payment_analysis.sort_values(
    "Churn_Rate",
    ascending=False
)

print(
    payment_analysis.to_string(
        index=False
    )
)


# ============================================================
# 12. CHURN BY CITY
# ============================================================

print("\n" + "=" * 70)
print("10. CHURN BY CITY")
print("=" * 70)

city_analysis = (
    df.groupby("City")
    .agg(
        Customers=("Customer_ID", "count"),
        Churned_Customers=(
            "Churn",
            lambda x: (x == "Yes").sum()
        )
    )
    .reset_index()
)

city_analysis["Churn_Rate"] = (
    city_analysis["Churned_Customers"]
    / city_analysis["Customers"]
    * 100
)

city_analysis = city_analysis.sort_values(
    "Churn_Rate",
    ascending=False
)

print(
    city_analysis.to_string(
        index=False
    )
)


# ============================================================
# 13. CHURN REASONS
# ============================================================

print("\n" + "=" * 70)
print("11. CHURN REASONS")
print("=" * 70)

reason_analysis = (
    df.loc[
        df["Churn"] == "Yes",
        "Churn_Reason"
    ]
    .value_counts()
    .reset_index()
)

reason_analysis.columns = [
    "Churn_Reason",
    "Customers"
]

reason_analysis["Percentage"] = (
    reason_analysis["Customers"]
    / reason_analysis["Customers"].sum()
    * 100
)

print(
    reason_analysis.to_string(
        index=False
    )
)


# ============================================================
# 14. HIGH-VALUE CHURN
# ============================================================

print("\n" + "=" * 70)
print("12. HIGH-VALUE CUSTOMER CHURN")
print("=" * 70)

customer_value_threshold = (
    df["Customer_Value"]
    .quantile(0.75)
)

high_value_customers = df[
    df["Customer_Value"]
    >= customer_value_threshold
]

high_value_churn_rate = (
    high_value_customers["Churn"]
    .eq("Yes")
    .mean()
    * 100
)

print(
    f"75th percentile Customer Value: "
    f"₹{customer_value_threshold:,.2f}"
)

print(
    f"High-value customers: "
    f"{len(high_value_customers):,}"
)

print(
    f"High-value customer churn rate: "
    f"{high_value_churn_rate:.2f}%"
)


# ============================================================
# 15. SAVE ANALYSIS TABLES
# ============================================================

contract_analysis.to_csv(
    os.path.join(
        REPORT_DIR,
        "churn_by_contract.csv"
    ),
    index=False
)

plan_analysis.to_csv(
    os.path.join(
        REPORT_DIR,
        "churn_by_plan.csv"
    ),
    index=False
)

tenure_analysis.to_csv(
    os.path.join(
        REPORT_DIR,
        "churn_by_tenure.csv"
    ),
    index=False
)

reason_analysis.to_csv(
    os.path.join(
        REPORT_DIR,
        "churn_reasons.csv"
    ),
    index=False
)

print("\n" + "=" * 70)
print("EDA COMPLETE")
print("=" * 70)