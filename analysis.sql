-- 1. Total revenue and profit
SELECT 
    SUM(Sales) AS total_revenue,
    SUM(Profit) AS total_profit
FROM sales_data;

-- 2. Revenue by region
SELECT 
    Region,
    SUM(Sales) AS revenue
FROM sales_data
GROUP BY Region
ORDER BY revenue DESC;

-- 3. Top 10 customers by revenue
SELECT 
    Customer_Name,
    SUM(Sales) AS total_spent
FROM sales_data
GROUP BY Customer_Name
ORDER BY total_spent DESC
LIMIT 10;

-- 4. Profitability by category
SELECT 
    Category,
    SUM(Profit) AS profit
FROM sales_data
GROUP BY Category
ORDER BY profit DESC;

-- 5. Orders with negative profit (loss-making)
SELECT 
    Order_ID,
    Sales,
    Profit
FROM sales_data
WHERE Profit < 0;

-- 6. Average order value
SELECT 
    AVG(Sales) AS avg_order_value
FROM sales_data;
