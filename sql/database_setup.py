import os
import sqlite3
import pandas as pd


# ============================================================
# TELECOM CUSTOMER CHURN
# SQLITE DATABASE SETUP
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

SQL_DIR = os.path.join(
    BASE_DIR,
    "sql"
)

os.makedirs(
    SQL_DIR,
    exist_ok=True
)

DB_PATH = os.path.join(
    SQL_DIR,
    "telecom_churn.db"
)


print("=" * 70)
print("TELECOM CHURN - SQLITE DATABASE SETUP")
print("=" * 70)


# ============================================================
# 1. CONNECT TO DATABASE
# ============================================================

connection = sqlite3.connect(DB_PATH)

print(f"\nDatabase created:")
print(DB_PATH)


# ============================================================
# 2. LOAD PROCESSED CSV FILES
# ============================================================

customers = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "customers_clean.csv"
    )
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

customer_status = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "customer_status_clean.csv"
    )
)


# ============================================================
# 3. WRITE TABLES
# ============================================================

print("\nLoading tables...")


customers.to_sql(
    "customers",
    connection,
    if_exists="replace",
    index=False
)

print(
    f"customers       : {len(customers):,} rows"
)


subscriptions.to_sql(
    "subscriptions",
    connection,
    if_exists="replace",
    index=False
)

print(
    f"subscriptions   : {len(subscriptions):,} rows"
)


usage.to_sql(
    "usage",
    connection,
    if_exists="replace",
    index=False
)

print(
    f"usage           : {len(usage):,} rows"
)


customer_status.to_sql(
    "customer_status",
    connection,
    if_exists="replace",
    index=False
)

print(
    f"customer_status : {len(customer_status):,} rows"
)


# ============================================================
# 4. CREATE INDEXES
# ============================================================

print("\nCreating indexes...")


cursor = connection.cursor()

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_customers_id
    ON customers(Customer_ID)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_subscriptions_id
    ON subscriptions(Customer_ID)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_usage_id
    ON usage(Customer_ID)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_status_id
    ON customer_status(Customer_ID)
""")


connection.commit()


# ============================================================
# 5. VERIFY TABLES
# ============================================================

print("\nVerifying database...")

tables = cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""").fetchall()

for table in tables:
    print(
        f"✓ {table[0]}"
    )


# ============================================================
# 6. VERIFY ROW COUNTS
# ============================================================

print("\nRow counts:")

for table_name in [
    "customers",
    "subscriptions",
    "usage",
    "customer_status"
]:

    count = cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]

    print(
        f"{table_name:<20}: {count:,}"
    )


# ============================================================
# 7. CLOSE
# ============================================================

connection.close()

print("\n" + "=" * 70)
print("DATABASE SETUP COMPLETE")
print("=" * 70)