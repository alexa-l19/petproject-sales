-- 1. Ключевые показатели
SELECT COUNT(*)                                   AS orders_cnt,
       COUNT(DISTINCT customer_id)                AS customers,
       SUM(revenue)                               AS revenue,
       SUM(profit)                                AS profit,
       ROUND(SUM(profit) / SUM(revenue) * 100, 1) AS margin_pct,
       ROUND(SUM(revenue) / COUNT(*))             AS avg_check
FROM orders;

-- 2. Категории: выручка, маржа и доли в выручке и прибыли
SELECT category,
       SUM(revenue)                                                AS revenue,
       SUM(profit)                                                 AS profit,
       ROUND(SUM(profit) / SUM(revenue) * 100, 1)                  AS margin_pct,
       ROUND(SUM(revenue) / SUM(SUM(revenue)) OVER () * 100, 1)    AS revenue_share_pct,
       ROUND(SUM(profit)  / SUM(SUM(profit))  OVER () * 100, 1)    AS profit_share_pct
FROM orders
GROUP BY category
ORDER BY revenue DESC;

-- 3. Динамика по месяцам
SELECT DATE_TRUNC('month', order_date)::date AS month,
       SUM(revenue) AS revenue,
       SUM(profit)  AS profit
FROM orders
GROUP BY 1
ORDER BY 1;

-- 4. Матрица «категория x скидка»
SELECT category,
       discount,
       SUM(revenue) AS revenue,
       SUM(profit)  AS profit,
       ROUND(SUM(profit) / SUM(revenue) * 100, 1) AS margin_pct
FROM orders
GROUP BY category, discount
ORDER BY category, discount;

-- 5. Регионы
SELECT region,
       SUM(revenue) AS revenue,
       SUM(profit)  AS profit,
       ROUND(SUM(profit) / SUM(revenue) * 100, 1) AS margin_pct
FROM orders
GROUP BY region
ORDER BY revenue DESC;

-- 6. Топ-10 клиентов
SELECT customer_id,
       COUNT(*)     AS orders_cnt,
       SUM(revenue) AS revenue,
       SUM(profit)  AS profit
FROM orders
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 10;
