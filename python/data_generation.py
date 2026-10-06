import os
import numpy as np
import pandas as pd

# ============================================================
# CUSTOMER CHURN ANALYTICS
# Synthetic Dataset Generator
# ============================================================

# -----------------------------
# Configuration
# -----------------------------

SEED = 42
N_CUSTOMERS = 250_000

np.random.seed(SEED)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DIR, exist_ok=True)


# ============================================================
# 1. CUSTOMER MASTER TABLE
# ============================================================

print("Generating customers...")

customer_ids = [
    f"CUST{i:06d}"
    for i in range(1, N_CUSTOMERS + 1)
]

# Demographics
gender = np.random.choice(
    ["Male", "Female", "Other"],
    size=N_CUSTOMERS,
    p=[0.49, 0.49, 0.02]
)

age = np.clip(
    np.random.normal(loc=34, scale=10, size=N_CUSTOMERS),
    18,
    70
).astype(int)


# Locations
locations = [
    ("Hyderabad", "Telangana"),
    ("Bengaluru", "Karnataka"),
    ("Chennai", "Tamil Nadu"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Gurugram", "Haryana"),
    ("Noida", "Uttar Pradesh"),
    ("Kolkata", "West Bengal"),
    ("Ahmedabad", "Gujarat"),
    ("Jaipur", "Rajasthan"),
    ("Kochi", "Kerala"),
]

location_probs = [
    0.16, 0.14, 0.09, 0.11,
    0.08, 0.09, 0.06, 0.05,
    0.07, 0.06, 0.05, 0.04
]

location_indices = np.random.choice(
    len(locations),
    size=N_CUSTOMERS,
    p=location_probs
)

cities = np.array([locations[i][0] for i in location_indices])
states = np.array([locations[i][1] for i in location_indices])


# Join dates
join_start = pd.Timestamp("2023-01-01")
join_end = pd.Timestamp("2026-03-31")

days_range = (join_end - join_start).days

random_days = np.random.randint(
    0,
    days_range + 1,
    size=N_CUSTOMERS
)

join_dates = (
    join_start
    + pd.to_timedelta(random_days, unit="D")
)


# Tenure calculated relative to analysis date
analysis_date = pd.Timestamp("2026-09-01")

tenure_months = (
    (analysis_date - join_dates).days / 30.44
).astype(int)

tenure_months = np.clip(
    tenure_months,
    1,
    44
)


customers = pd.DataFrame({
    "Customer_ID": customer_ids,
    "Gender": gender,
    "Age": age,
    "City": cities,
    "State": states,
    "Join_Date": join_dates,
    "Tenure_Months": tenure_months
})


# ============================================================
# 2. SUBSCRIPTION TABLE
# ============================================================

print("Generating subscriptions...")

plans = np.random.choice(
    ["Basic", "Standard", "Premium"],
    size=N_CUSTOMERS,
    p=[0.35, 0.45, 0.20]
)

contract_type = np.random.choice(
    ["Monthly", "Quarterly", "Annual"],
    size=N_CUSTOMERS,
    p=[0.55, 0.25, 0.20]
)

# Base price according to plan
base_prices = {
    "Basic": 399,
    "Standard": 699,
    "Premium": 1099
}

monthly_charges = np.array([
    base_prices[p] for p in plans
], dtype=float)

# Add realistic price variation
monthly_charges += np.random.normal(
    0,
    60,
    N_CUSTOMERS
)

monthly_charges = np.clip(
    monthly_charges,
    199,
    1499
)

monthly_charges = np.round(
    monthly_charges,
    2
)


payment_method = np.random.choice(
    [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Net Banking",
        "Wallet"
    ],
    size=N_CUSTOMERS,
    p=[0.38, 0.28, 0.14, 0.12, 0.08]
)


auto_renewal = np.random.choice(
    ["Yes", "No"],
    size=N_CUSTOMERS,
    p=[0.72, 0.28]
)


subscriptions = pd.DataFrame({
    "Customer_ID": customer_ids,
    "Plan": plans,
    "Contract_Type": contract_type,
    "Monthly_Charges": monthly_charges,
    "Payment_Method": payment_method,
    "Auto_Renewal": auto_renewal
})


# ============================================================
# 3. USAGE / BEHAVIOR TABLE
# ============================================================

print("Generating customer behavior...")

# Customer engagement increases somewhat with tenure,
# but contains substantial randomness.

tenure_effect = np.sqrt(tenure_months)

avg_monthly_usage = (
    18
    + tenure_effect * 2
    + np.random.normal(0, 8, N_CUSTOMERS)
)

avg_monthly_usage = np.clip(
    avg_monthly_usage,
    2,
    80
)

avg_monthly_usage = np.round(
    avg_monthly_usage,
    2
)


monthly_logins = (
    avg_monthly_usage * 0.65
    + np.random.normal(0, 5, N_CUSTOMERS)
)

monthly_logins = np.clip(
    monthly_logins,
    1,
    60
).astype(int)


# Support tickets
support_tickets = np.random.poisson(
    lam=2.2,
    size=N_CUSTOMERS
)

# Add a small relationship between low usage and support demand
low_usage_mask = avg_monthly_usage < 15

support_tickets[low_usage_mask] += np.random.binomial(
    2,
    0.25,
    low_usage_mask.sum()
)

support_tickets = np.clip(
    support_tickets,
    0,
    15
)


# Response time
avg_response_time = (
    np.random.gamma(
        shape=2.2,
        scale=2.0,
        size=N_CUSTOMERS
    )
)

avg_response_time = np.clip(
    avg_response_time,
    0.5,
    24
)

avg_response_time = np.round(
    avg_response_time,
    2
)


# Downtime
downtime_hours = np.random.gamma(
    shape=1.5,
    scale=1.2,
    size=N_CUSTOMERS
)

downtime_hours = np.clip(
    downtime_hours,
    0,
    15
)

downtime_hours = np.round(
    downtime_hours,
    2
)


usage = pd.DataFrame({
    "Customer_ID": customer_ids,
    "Avg_Monthly_Usage_Hours": avg_monthly_usage,
    "Monthly_Logins": monthly_logins,
    "Support_Tickets": support_tickets,
    "Avg_Response_Time_Hours": avg_response_time,
    "Downtime_Hours": downtime_hours
})


# ============================================================
# 4. SATISFACTION SCORE
# ============================================================

print("Generating satisfaction scores...")

# Satisfaction influenced by support experience,
# downtime and usage, with random variation.

satisfaction_raw = (
    8.2
    - support_tickets * 0.12
    - downtime_hours * 0.10
    + avg_monthly_usage * 0.015
    + np.random.normal(0, 1.1, N_CUSTOMERS)
)

satisfaction_score = np.clip(
    np.round(satisfaction_raw),
    1,
    10
).astype(int)


# ============================================================
# 5. CHURN PROBABILITY
# ============================================================

print("Generating churn outcomes...")

# IMPORTANT:
# We are NOT using a simple deterministic rule.
# Multiple variables contribute to churn probability.

risk_score = np.zeros(N_CUSTOMERS)


# Contract effect
risk_score += np.where(
    contract_type == "Monthly",
    0.75,
    np.where(
        contract_type == "Quarterly",
        0.25,
        -0.45
    )
)


# Satisfaction effect
risk_score += np.where(
    satisfaction_score <= 4,
    1.15,
    np.where(
        satisfaction_score <= 6,
        0.55,
        np.where(
            satisfaction_score >= 9,
            -0.45,
            0
        )
    )
)


# Usage effect
risk_score += np.where(
    avg_monthly_usage < 10,
    0.85,
    np.where(
        avg_monthly_usage < 20,
        0.35,
        np.where(
            avg_monthly_usage > 55,
            -0.25,
            0
        )
    )
)


# Support tickets
risk_score += np.where(
    support_tickets >= 7,
    0.75,
    np.where(
        support_tickets >= 4,
        0.30,
        0
    )
)


# Downtime
risk_score += np.where(
    downtime_hours >= 7,
    0.65,
    np.where(
        downtime_hours >= 4,
        0.30,
        0
    )
)


# Price sensitivity
risk_score += np.where(
    (monthly_charges > 1000) &
    (avg_monthly_usage < 20),
    0.65,
    0
)


# Auto renewal
risk_score += np.where(
    auto_renewal == "No",
    0.30,
    -0.10
)


# Tenure effect
risk_score += np.where(
    tenure_months <= 6,
    0.35,
    np.where(
        tenure_months >= 30,
        -0.25,
        0
    )
)


# Random noise
risk_score += np.random.normal(
    0,
    0.65,
    N_CUSTOMERS
)


# Convert score into probability
base_logit = -2.25

churn_probability = (
    1 /
    (
        1 +
        np.exp(
            -(base_logit + risk_score)
        )
    )
)


# Generate actual churn outcome
churn_flag = (
    np.random.random(N_CUSTOMERS)
    < churn_probability
)


churn = np.where(
    churn_flag,
    "Yes",
    "No"
)


# ============================================================
# 6. CHURN DATE
# ============================================================

churn_dates = pd.Series(
    pd.NaT,
    index=range(N_CUSTOMERS),
    dtype="datetime64[ns]"
)

churned_indices = np.where(churn_flag)[0]

for idx in churned_indices:

    join_date = join_dates[idx]

    minimum_date = join_date + pd.Timedelta(days=30)

    maximum_date = analysis_date

    if minimum_date <= maximum_date:

        days_available = (
            maximum_date - minimum_date
        ).days

        random_offset = np.random.randint(
            0,
            max(days_available, 1) + 1
        )

        churn_dates[idx] = (
            minimum_date
            + pd.Timedelta(days=int(random_offset))
        )


# ============================================================
# 7. CHURN REASONS
# ============================================================

print("Generating churn reasons...")

churn_reasons = np.full(
    N_CUSTOMERS,
    None,
    dtype=object
)

for idx in churned_indices:

    # Reason influenced by customer behavior,
    # but not perfectly deterministic.

    if (
        monthly_charges[idx] > 1000
        and avg_monthly_usage[idx] < 20
    ):
        reason = np.random.choice(
            ["High Price", "Competitor"],
            p=[0.65, 0.35]
        )

    elif support_tickets[idx] >= 7:
        reason = np.random.choice(
            ["Poor Support", "Technical Issues"],
            p=[0.65, 0.35]
        )

    elif downtime_hours[idx] >= 7:
        reason = np.random.choice(
            ["Technical Issues", "Poor Service"],
            p=[0.70, 0.30]
        )

    elif satisfaction_score[idx] <= 4:
        reason = np.random.choice(
            ["Poor Service", "Poor Support", "High Price"],
            p=[0.40, 0.35, 0.25]
        )

    elif avg_monthly_usage[idx] < 10:
        reason = np.random.choice(
            ["Low Usage", "Competitor", "Other"],
            p=[0.55, 0.30, 0.15]
        )

    else:
        reason = np.random.choice(
            [
                "Competitor",
                "High Price",
                "Payment Issues",
                "Relocation",
                "Other"
            ],
            p=[0.25, 0.25, 0.15, 0.10, 0.25]
        )

    churn_reasons[idx] = reason


# ============================================================
# 8. CUSTOMER VALUE
# ============================================================

customer_value = (
    monthly_charges
    * np.maximum(tenure_months, 1)
)

# Add realistic variation
customer_value *= np.random.normal(
    1.0,
    0.08,
    N_CUSTOMERS
)

customer_value = np.round(
    customer_value,
    2
)


# ============================================================
# 9. CUSTOMER STATUS TABLE
# ============================================================

customer_status = pd.DataFrame({
    "Customer_ID": customer_ids,
    "Churn": churn,
    "Churn_Date": churn_dates,
    "Churn_Reason": churn_reasons,
    "Satisfaction_Score": satisfaction_score,
    "Customer_Value": customer_value
})


# ============================================================
# 10. INTRODUCE SMALL DATA QUALITY ISSUES
# ============================================================

print("Introducing controlled data-quality issues...")

# We intentionally introduce a small number of issues.
# Later, our cleaning stage will detect and fix them.

missing_ticket_indices = np.random.choice(
    N_CUSTOMERS,
    size=int(N_CUSTOMERS * 0.002),
    replace=False
)

usage.loc[
    missing_ticket_indices,
    "Support_Tickets"
] = np.nan


missing_satisfaction_indices = np.random.choice(
    N_CUSTOMERS,
    size=int(N_CUSTOMERS * 0.001),
    replace=False
)

customer_status.loc[
    missing_satisfaction_indices,
    "Satisfaction_Score"
] = np.nan


# ============================================================
# 11. SAVE DATA
# ============================================================

print("Saving files...")

customers.to_csv(
    os.path.join(RAW_DIR, "customers.csv"),
    index=False
)

subscriptions.to_csv(
    os.path.join(RAW_DIR, "subscriptions.csv"),
    index=False
)

usage.to_csv(
    os.path.join(RAW_DIR, "usage.csv"),
    index=False
)

customer_status.to_csv(
    os.path.join(RAW_DIR, "customer_status.csv"),
    index=False
)


# ============================================================
# 12. SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATASET GENERATION COMPLETE")
print("=" * 60)

print(f"Customers: {len(customers):,}")
print(f"Subscriptions: {len(subscriptions):,}")
print(f"Usage records: {len(usage):,}")
print(f"Status records: {len(customer_status):,}")

print("\nChurn distribution:")

print(
    customer_status["Churn"]
    .value_counts()
)

print("\nChurn rate:")

print(
    f"{(churn_flag.mean() * 100):.2f}%"
)

print("\nFiles saved to:")

print(RAW_DIR)

print("=" * 60)