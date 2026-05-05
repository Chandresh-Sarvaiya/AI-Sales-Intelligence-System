--How business is going??

--total revenue
select sum(price*quantity) from online_retail;

--total customers
select count(distinct customer_id)from online_retail;

--total orders
select count(distinct invoice) from online_retail;

--average revenue per order
select sum(price*quantity)/count(distinct invoice) as Average_order_value
from online_retail;

--revenue per month
select date_trunc('month',invoice_date) as month,
sum(price*quantity) as revenue
from online_retail
group by month
order by month; 

--top months generating high revenue
select date_trunc('month',invoice_date) as month,
sum(price*quantity) as revenue
from online_retail
group by month
order by revenue desc
limit 3;

--revenue as per country
select country, sum(price*quantity) as revenue
from online_retail
group by country
order by revenue desc;

--total orders per country
select country, count(distinct invoice) as Total_orders
from online_retail
group by country
order by Total_orders desc;

--sum of quantity of different products 
select product, sum(quantity)as Total_quantity
from online_retail
group by product
order by Total_quantity desc
limit 10;

-- best-selling products
select product, sum(price*quantity) as Total_revenue
from online_retail
group by product
order by Total_revenue desc
limit 10;

--total number of products
select count(distinct product) as Total_Products 
from online_retail;

--transactions generating highest revenue
select invoice, sum(quantity*price) as Revenue
from online_retail
group by invoice
order by Revenue desc
limit 10;

--average revenue per transaction
select avg(revenue) as avg_revenue_per_transaction
from (
select invoice, sum(price*quantity) as revenue
from online_retail
group by invoice
) as transaction_revenue;

--customers generating maximum revenue
select customer_id, count(distinct invoice) as Total_orders, sum(price*quantity) as revenue
from online_retail
group by customer_id
order by revenue desc;