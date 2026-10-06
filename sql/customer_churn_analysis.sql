-- ============================================================
-- TELECOM CUSTOMER CHURN
-- CUSTOMER-LEVEL ANALYTICAL DATASET
-- ============================================================
DROP VIEW IF EXISTS customer_churn_analysis;
CREATE VIEW customer_churn_analysis AS
SELECT -- ========================================================
    -- CUSTOMER INFORMATION
    -- ========================================================
    c.Customer_ID,
    c.Gender,
    c.Age,
    c.City,
    c.State,
    c.Join_Date,
    c.Tenure_Months,
    -- ========================================================
    -- SUBSCRIPTION INFORMATION
    -- ========================================================
    s.Plan,
    s.Contract_Type,
    s.Monthly_Charges,
    s.Payment_Method,
    s.Auto_Renewal,
    -- ========================================================
    -- USAGE & SERVICE INFORMATION
    -- ========================================================
    u.Avg_Monthly_Usage_Hours,
    u.Monthly_Logins,
    u.Support_Tickets,
    u.Avg_Response_Time_Hours,
    u.Downtime_Hours,
    -- ========================================================
    -- CHURN INFORMATION
    -- ========================================================
    cs.Churn,
    cs.Churn_Date,
    cs.Churn_Reason,
    cs.Satisfaction_Score,
    cs.Customer_Value,
    -- ========================================================
    -- DERIVED TENURE GROUP
    -- ========================================================
    CASE
        WHEN c.Tenure_Months <= 6 THEN '0-6 Months'
        WHEN c.Tenure_Months <= 12 THEN '7-12 Months'
        WHEN c.Tenure_Months <= 24 THEN '13-24 Months'
        WHEN c.Tenure_Months <= 36 THEN '25-36 Months'
        ELSE '37+ Months'
    END AS Tenure_Group,
    -- ========================================================
    -- DERIVED USAGE GROUP
    -- ========================================================
    CASE
        WHEN u.Avg_Monthly_Usage_Hours < 10 THEN '<10 Hours'
        WHEN u.Avg_Monthly_Usage_Hours < 20 THEN '10-20 Hours'
        WHEN u.Avg_Monthly_Usage_Hours < 40 THEN '20-40 Hours'
        WHEN u.Avg_Monthly_Usage_Hours < 60 THEN '40-60 Hours'
        ELSE '60+ Hours'
    END AS Usage_Group,
    -- ========================================================
    -- DERIVED SUPPORT GROUP
    -- ========================================================
    CASE
        WHEN u.Support_Tickets <= 1 THEN '0-1 Tickets'
        WHEN u.Support_Tickets <= 3 THEN '2-3 Tickets'
        WHEN u.Support_Tickets <= 5 THEN '4-5 Tickets'
        ELSE '6+ Tickets'
    END AS Support_Group,
    -- ========================================================
    -- DERIVED DOWNTIME GROUP
    -- ========================================================
    CASE
        WHEN u.Downtime_Hours < 2 THEN '0-2 Hours'
        WHEN u.Downtime_Hours < 4 THEN '2-4 Hours'
        WHEN u.Downtime_Hours < 7 THEN '4-7 Hours'
        ELSE '7+ Hours'
    END AS Downtime_Group,
    -- ========================================================
    -- CHURN FLAG
    -- Useful for Power BI calculations
    -- ========================================================
    CASE
        WHEN cs.Churn = 'Yes' THEN 1
        ELSE 0
    END AS Churn_Flag
FROM customers c
    INNER JOIN subscriptions s ON c.Customer_ID = s.Customer_ID
    INNER JOIN usage u ON c.Customer_ID = u.Customer_ID
    INNER JOIN customer_status cs ON c.Customer_ID = cs.Customer_ID;