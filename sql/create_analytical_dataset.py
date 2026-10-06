import os
import sqlite3
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SQL_DIR = os.path.join(
    BASE_DIR,
    "sql"
)

DB_PATH = os.path.join(
    SQL_DIR,
    "telecom_churn.db"
)

SQL_FILE = os.path.join(
    SQL_DIR,
    "customer_churn_analysis.sql"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "customer_churn_analysis.csv"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("CUSTOMER CHURN ANALYTICAL DATASET")
print("=" * 70)


# ============================================================
# CONNECT
# ============================================================

connection = sqlite3.connect(DB_PATH)


# ============================================================
# READ SQL
# ============================================================

with open(
    SQL_FILE,
    "r",
    encoding="utf-8"
) as file:

    sql_script = file.read()


# ============================================================
# CREATE VIEW
# ============================================================

connection.executescript(
    sql_script
)

connection.commit()


print("\n✓ Analytical view created")


# ============================================================
# VALIDATE ROW COUNT
# ============================================================

row_count = connection.execute(
    """
    SELECT COUNT(*)
    FROM customer_churn_analysis
    """
).fetchone()[0]


print(
    f"Analytical rows : {row_count:,}"
)


# ============================================================
# VALIDATE CUSTOMER IDs
# ============================================================

unique_ids = connection.execute(
    """
    SELECT COUNT(DISTINCT Customer_ID)
    FROM customer_churn_analysis
    """
).fetchone()[0]


print(
    f"Unique customers: {unique_ids:,}"
)


# ============================================================
# VALIDATE DUPLICATES
# ============================================================

duplicate_ids = connection.execute(
    """
    SELECT COUNT(*)
    FROM (
        SELECT Customer_ID
        FROM customer_churn_analysis
        GROUP BY Customer_ID
        HAVING COUNT(*) > 1
    )
    """
).fetchone()[0]


print(
    f"Duplicate IDs   : {duplicate_ids:,}"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_sql_query(
    """
    SELECT *
    FROM customer_churn_analysis
    """,
    connection
)


# ============================================================
# DATASET INFORMATION
# ============================================================

print(
    f"Columns         : {len(df.columns):,}"
)

print("\nColumns:")

for column in df.columns:

    print(
        f"  ✓ {column}"
    )


# ============================================================
# CHURN VALIDATION
# ============================================================

churn_counts = df["Churn"].value_counts()

print("\nChurn distribution:")

print(churn_counts)


# ============================================================
# SAVE CSV
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved to:")

print(
    OUTPUT_FILE
)


# ============================================================
# CLOSE
# ============================================================

connection.close()


print("\n" + "=" * 70)
print("ANALYTICAL DATASET COMPLETE")
print("=" * 70)