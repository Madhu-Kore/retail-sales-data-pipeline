CREATE OR REPLACE VIEW monthly_sales AS
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.sales_amount), 2) AS total_sales,
    ROUND(SUM(f.profit_amount), 2) AS total_profit,
    COUNT(DISTINCT f.order_id) AS order_count
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name;

CREATE OR REPLACE VIEW category_performance AS
SELECT
    p.category,
    ROUND(SUM(f.sales_amount), 2) AS total_sales,
    ROUND(SUM(f.profit_amount), 2) AS total_profit,
    SUM(f.quantity) AS units_sold
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category;
