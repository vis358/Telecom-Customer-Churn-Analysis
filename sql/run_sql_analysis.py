import os
import sqlite3


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
    "business_analysis.sql"
)


# ============================================================
# CONNECT TO SQLITE
# ============================================================

connection = sqlite3.connect(DB_PATH)


# ============================================================
# READ SQL FILE
# ============================================================

with open(
    SQL_FILE,
    "r",
    encoding="utf-8"
) as file:

    sql_script = file.read()


# ============================================================
# SPLIT QUERIES
# ============================================================

statements = [
    statement.strip()
    for statement in sql_script.split(";")
    if statement.strip()
]


print("=" * 70)
print("TELECOM CHURN - SQL BUSINESS ANALYSIS")
print("=" * 70)


# ============================================================
# EXECUTE EACH QUERY
# ============================================================

query_number = 0

for statement in statements:

    # Ignore comment-only sections
    executable_lines = [
        line.strip()
        for line in statement.splitlines()
        if line.strip()
        and not line.strip().startswith("--")
    ]

    if not executable_lines:
        continue

    query_number += 1

    try:

        cursor = connection.execute(statement)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        print("\n" + "=" * 70)
        print(f"QUERY {query_number}")
        print("=" * 70)

        print(" | ".join(columns))

        print("-" * 70)

        for row in rows:

            print(
                " | ".join(
                    str(value)
                    for value in row
                )
            )

    except Exception as error:

        print("\n" + "=" * 70)
        print(f"ERROR IN QUERY {query_number}")
        print("=" * 70)

        print(error)


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()


print("\n" + "=" * 70)
print("SQL ANALYSIS COMPLETE")
print("=" * 70)