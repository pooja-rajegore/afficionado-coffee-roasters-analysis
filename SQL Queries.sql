select *from "Retail_data"

-- 1. High-Volume Products with Low Revenue Contribution

WITH product_analysis AS
(
    SELECT
        product_detail,
        SUM(transaction_qty) AS units_sold,
        SUM(revenue) AS total_revenue,
        RANK() OVER (
            ORDER BY SUM(transaction_qty) DESC
        ) AS volume_rank,

        RANK() OVER (
            ORDER BY SUM(revenue) DESC
        ) AS revenue_rank

    FROM "Retail_data"
    GROUP BY product_detail
)
SELECT *
FROM product_analysis
WHERE volume_rank <= 10
AND revenue_rank > 20;


-- High-Priced Products with Low Sales Frequency
WITH premium_products AS
(
    SELECT
        product_detail,
        AVG(unit_price) AS avg_price,
        SUM(transaction_qty) AS units_sold
    FROM "Retail_data"
    GROUP BY product_detail
)
SELECT *
FROM premium_products
ORDER BY avg_price DESC,
         units_sold ASC;
		 

-- Overcrowded Menu Analysis
-- Bottom 20 Products
SELECT
    product_detail,
    ROUND(SUM(revenue)::numeric,2) AS total_revenue
FROM "Retail_data"
GROUP BY product_detail
ORDER BY total_revenue ASC
LIMIT 20;

-- Which products customers prefer
-- Top 10 Preferred Products
SELECT
    product_detail,
    SUM(transaction_qty) AS units_sold
FROM "Retail_data"
GROUP BY product_detail
ORDER BY units_sold DESC
LIMIT 10;


-- Which Products Generate the Most Revenue?
SELECT
    product_detail,
    ROUND(SUM(revenue)::numeric,2) AS total_revenue
FROM "Retail_data"
GROUP BY product_detail
ORDER BY total_revenue DESC
LIMIT 10;

-- How Revenue Is Distributed Across Categories?
SELECT
    product_category,
    ROUND(SUM(revenue)::numeric,2) AS category_revenue,
    ROUND(
	(
        SUM(revenue) * 100.0 /
        SUM(SUM(revenue)) OVER ()
		)::numeric,
        2
    ) AS revenue_share_pct
FROM public."Retail_data" 
GROUP BY product_category
ORDER BY category_revenue DESC;


-- How Revenue Is Distributed Across Variants?
-- Top Variants in Each Category
SELECT
    product_category,
    product_detail,
    ROUND(SUM(revenue)::numeric,2) AS total_revenue
FROM "Retail_data"
GROUP BY
    product_category,
    product_detail
ORDER BY
    product_category,
    total_revenue DESC;

--Primary Objective :

-- 1.Identify Top-Selling and Least-Selling Products

-- Top-Selling Products (by Units Sold)
SELECT
    product_detail,
    SUM(transaction_qty) AS units_sold
FROM "Retail_data"
GROUP BY product_detail
ORDER BY units_sold DESC
LIMIT 10;

-- Least-Selling Products
SELECT
    product_detail,
    SUM(transaction_qty) AS units_sold
FROM "Retail_data"
GROUP BY product_detail
ORDER BY units_sold ASC
LIMIT 10;

-- 2. Quantify Revenue Contribution by Product and Category

-- Revenue Contribution by Product
SELECT
    product_detail,
    ROUND(SUM(revenue)::numeric, 2) AS total_revenue,
    ROUND(
        (
            SUM(revenue) * 100.0
            / SUM(SUM(revenue)) OVER ()
        )::numeric,
        2
    ) AS revenue_contribution_pct
FROM "Retail_data"
GROUP BY product_detail
ORDER BY total_revenue DESC;

-- Revenue Contribution by Category
SELECT
    product_category,
    ROUND(SUM(revenue)::numeric,2) AS category_revenue,
    ROUND(
	(
        SUM(revenue) * 100.0 /
        SUM(SUM(revenue)) OVER ()
		)::numeric,
        2
    ) AS category_share_pct
FROM "Retail_data"
GROUP BY product_category
ORDER BY category_revenue DESC;

-- 3 Measure Revenue Concentration Across the Menu

WITH product_revenue AS
(
    SELECT
        product_detail,
        SUM(revenue) AS revenue
    FROM "Retail_data"
    GROUP BY product_detail
),
top5 AS
(
    SELECT SUM(revenue) AS top5_revenue
    FROM
    (
        SELECT revenue
        FROM product_revenue
        ORDER BY revenue DESC
        LIMIT 5
    ) t
),
total AS
(
    SELECT SUM(revenue) AS total_revenue
    FROM product_revenue
)

SELECT
ROUND(
(
    top5.top5_revenue * 100.0 /
    total.total_revenue
)::numeric,
    2
) AS revenue_concentration_ratio
FROM top5,total;

-- Secondary Objectives:
-- 1. Support Menu Simplification and Optimization
SELECT
    product_detail,
    ROUND(SUM(revenue)::numeric,2) AS total_revenue
FROM "Retail_data"
GROUP BY product_detail
ORDER BY total_revenue ASC
LIMIT 10;


-- 2. Identify High-Impact "Hero" Products
-- Business Question
-- Which products generate the highest revenue and have strong customer demand?

SELECT
    product_detail,
    SUM(transaction_qty) AS units_sold,
    ROUND(SUM(revenue)::numeric,2) AS total_revenue
FROM "Retail_data"
GROUP BY product_detail
ORDER BY total_revenue DESC
LIMIT 10;

-- Advanced  High-Impact "Hero" Products
WITH product_performance AS
(
    SELECT
        product_detail,
        SUM(transaction_qty) AS units_sold,
        SUM(revenue) AS total_revenue
    FROM "Retail_data"
    GROUP BY product_detail
)

SELECT *
FROM product_performance
ORDER BY total_revenue DESC,
         units_sold DESC;
		 

-- 3. Highlight Low-Performing Products for Review or Redesign
-- Business Question
-- Which products have both low sales volume and low revenue?
-- Bottom Performer
SELECT
    product_detail,
    SUM(transaction_qty) AS units_sold,
    ROUND(SUM(revenue)::numeric,2) AS total_revenue
FROM "Retail_data"
GROUP BY product_detail
ORDER BY total_revenue ASC
LIMIT 15;


-- Problem Statements:

-- 1. Clear Visibility into Product Popularity vs Profitability
-- Business Question
-- Are the most popular products also the most profitable?

SELECT
    product_detail,
    SUM(transaction_qty) AS units_sold,
    ROUND(SUM(revenue)::numeric,2) AS total_revenue
FROM "Retail_data"
GROUP BY product_detail
ORDER BY units_sold DESC;

-- Advanced Analysis: Compare Popularity Rank vs Revenue Rank
WITH product_performance AS
(
    SELECT
        product_detail,
        SUM(transaction_qty) AS units_sold,
          ROUND(SUM(revenue)::numeric,2) AS total_revenue,

        RANK() OVER(
            ORDER BY SUM(transaction_qty) DESC
        ) AS popularity_rank,

        RANK() OVER(
            ORDER BY SUM(revenue) DESC
        ) AS profitability_rank

    FROM "Retail_data"
    GROUP BY product_detail
)

SELECT *
FROM product_performance
ORDER BY popularity_rank;

-- 2. Category-Level Revenue Dependency Insights

SELECT
    product_category,
    ROUND(SUM(revenue)::numeric,2) AS category_revenue,

    ROUND(
        (
            SUM(revenue) * 100.0 /
            SUM(SUM(revenue)) OVER()
        )::numeric,
        2
    ) AS revenue_share_pct

FROM "Retail_data"
GROUP BY product_category
ORDER BY category_revenue DESC;


-- 3. Identification of Low-Impact or Underperforming Menu Items

-- Find Products with Both Low Sales and Low Revenue

WITH product_performance AS
(
    SELECT
        product_detail,
        SUM(transaction_qty) AS units_sold,
        SUM(revenue) AS total_revenue
    FROM "Retail_data"
    GROUP BY product_detail
)

SELECT *
FROM product_performance
ORDER BY units_sold ASC,
         total_revenue ASC
LIMIT 15;








