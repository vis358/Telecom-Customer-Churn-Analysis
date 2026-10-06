-- ============================================================
-- TELECOM CUSTOMER CHURN ANALYTICS
-- SQL BUSINESS ANALYSIS
-- ============================================================
-- ============================================================
-- 1. OVERALL CHURN RATE
-- Business Question:
-- What percentage of customers have churned?
-- ============================================================
SELECT COUNT(*) AS total_customers,
    SUM(
        CASE
            WHEN Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate
FROM customer_status;
-- ============================================================
-- 2. CHURN BY CONTRACT TYPE
-- Business Question:
-- Which contract types have higher observed churn?
-- ============================================================
SELECT s.Contract_Type,
    COUNT(*) AS customers,
    SUM(
        CASE
            WHEN cs.Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN cs.Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate
FROM subscriptions s
    JOIN customer_status cs ON s.Customer_ID = cs.Customer_ID
GROUP BY s.Contract_Type
ORDER BY churn_rate DESC;
-- ============================================================
-- 3. CHURN BY TENURE GROUP
-- Business Question:
-- Which customer tenure groups have higher churn?
-- ============================================================
SELECT CASE
        WHEN c.Tenure_Months <= 6 THEN '0-6 Months'
        WHEN c.Tenure_Months <= 12 THEN '7-12 Months'
        WHEN c.Tenure_Months <= 24 THEN '13-24 Months'
        WHEN c.Tenure_Months <= 36 THEN '25-36 Months'
        ELSE '37+ Months'
    END AS tenure_group,
    COUNT(*) AS customers,
    SUM(
        CASE
            WHEN cs.Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN cs.Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate
FROM customers c
    JOIN customer_status cs ON c.Customer_ID = cs.Customer_ID
GROUP BY tenure_group
ORDER BY churn_rate DESC;
-- ============================================================
-- 4. CHURN BY SATISFACTION SCORE
-- Business Question:
-- How does satisfaction relate to observed churn?
-- ============================================================
SELECT cs.Satisfaction_Score,
    COUNT(*) AS customers,
    SUM(
        CASE
            WHEN cs.Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN cs.Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate
FROM customer_status cs
GROUP BY cs.Satisfaction_Score
ORDER BY cs.Satisfaction_Score;
-- ============================================================
-- 5. CHURN BY USAGE
-- Business Question:
-- Is lower engagement associated with higher churn?
-- ============================================================
SELECT CASE
        WHEN u.Avg_Monthly_Usage_Hours < 10 THEN '<10 Hours'
        WHEN u.Avg_Monthly_Usage_Hours < 20 THEN '10-20 Hours'
        WHEN u.Avg_Monthly_Usage_Hours < 40 THEN '20-40 Hours'
        WHEN u.Avg_Monthly_Usage_Hours < 60 THEN '40-60 Hours'
        ELSE '60+ Hours'
    END AS usage_group,
    COUNT(*) AS customers,
    SUM(
        CASE
            WHEN cs.Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN cs.Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate
FROM usage u
    JOIN customer_status cs ON u.Customer_ID = cs.Customer_ID
GROUP BY usage_group
ORDER BY churn_rate DESC;
-- ============================================================
-- 6. CHURN BY SUPPORT TICKETS
-- Business Question:
-- Does higher support interaction coincide with higher churn?
-- ============================================================
SELECT CASE
        WHEN u.Support_Tickets <= 1 THEN '0-1 Tickets'
        WHEN u.Support_Tickets <= 3 THEN '2-3 Tickets'
        WHEN u.Support_Tickets <= 5 THEN '4-5 Tickets'
        ELSE '6+ Tickets'
    END AS support_group,
    COUNT(*) AS customers,
    SUM(
        CASE
            WHEN cs.Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN cs.Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate
FROM usage u
    JOIN customer_status cs ON u.Customer_ID = cs.Customer_ID
GROUP BY support_group
ORDER BY churn_rate DESC;
-- ============================================================
-- 7. CHURN REASONS
-- Business Question:
-- Why are customers leaving?
-- ============================================================
SELECT Churn_Reason,
    COUNT(*) AS churned_customers,
    ROUND(
        100.0 * COUNT(*) / (
            SELECT COUNT(*)
            FROM customer_status
            WHERE Churn = 'Yes'
        ),
        2
    ) AS percentage_of_churn
FROM customer_status
WHERE Churn = 'Yes'
GROUP BY Churn_Reason
ORDER BY churned_customers DESC;
-- ============================================================
-- 8. MONTHLY CHARGE EXPOSURE
-- Business Question:
-- How much monthly charge exposure is associated with churned
-- customers?
-- ============================================================
SELECT cs.Churn,
    COUNT(*) AS customers,
    ROUND(
        SUM(s.Monthly_Charges),
        2
    ) AS monthly_charge_exposure,
    ROUND(
        AVG(s.Monthly_Charges),
        2
    ) AS average_monthly_charge
FROM subscriptions s
    JOIN customer_status cs ON s.Customer_ID = cs.Customer_ID
GROUP BY cs.Churn;
-- ============================================================
-- 9. HIGH-VALUE CUSTOMER CHURN
-- Business Question:
-- How does churn look among the top 25% of customers by
-- Customer Value?
-- ============================================================
WITH value_threshold AS (
    SELECT Customer_Value
    FROM customer_status
    ORDER BY Customer_Value
    LIMIT 1 OFFSET (
            SELECT CAST(
                    COUNT(*) * 0.75 AS INTEGER
                )
            FROM customer_status
        )
),
high_value_customers AS (
    SELECT cs.Customer_ID,
        cs.Customer_Value,
        cs.Churn
    FROM customer_status cs
    WHERE cs.Customer_Value >= (
            SELECT Customer_Value
            FROM value_threshold
        )
)
SELECT COUNT(*) AS high_value_customers,
    SUM(
        CASE
            WHEN Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_high_value_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS high_value_churn_rate
FROM high_value_customers;
-- ============================================================
-- 10. HIGH-RISK SEGMENTS
-- Business Question:
-- Which combinations of contract and tenure show higher
-- observed churn?
-- ============================================================
WITH customer_segments AS (
    SELECT c.Customer_ID,
        s.Contract_Type,
        CASE
            WHEN c.Tenure_Months <= 6 THEN '0-6 Months'
            WHEN c.Tenure_Months <= 12 THEN '7-12 Months'
            WHEN c.Tenure_Months <= 24 THEN '13-24 Months'
            WHEN c.Tenure_Months <= 36 THEN '25-36 Months'
            ELSE '37+ Months'
        END AS tenure_group,
        cs.Churn
    FROM customers c
        JOIN subscriptions s ON c.Customer_ID = s.Customer_ID
        JOIN customer_status cs ON c.Customer_ID = cs.Customer_ID
)
SELECT Contract_Type,
    tenure_group,
    COUNT(*) AS customers,
    SUM(
        CASE
            WHEN Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate
FROM customer_segments
GROUP BY Contract_Type,
    tenure_group
HAVING COUNT(*) >= 100
ORDER BY churn_rate DESC;