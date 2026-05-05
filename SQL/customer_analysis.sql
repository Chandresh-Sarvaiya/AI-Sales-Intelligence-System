--customer intellegnce analysis

--total orders per customer
select customer_id, count(distinct invoice) as Number_of_orders
from online_retail
group by customer_id;

--highest number of total orders by customers
select customer_id,count(distinct invoice) as Total_orders
from online_retail
group by customer_id 
order by Total_orders desc 
limit 10;

--customer generating highest revenue
select customer_id, sum(price*quantity) as Total_revenue
from online_retail
group by customer_id
order by Total_revenue desc
limit 10;

--revenue by each customer
select customer_id, sum(price*quantity) as Total_revenue
from online_retail
group by customer_id;

--first purchase of each customer
select customer_id,min(invoice_date) as First_purchase 
from online_retail
group by customer_id;

--last purchase of each customer
select customer_id, max(invoice_date) as Most_recent_purchase
from online_retail
group by customer_id;

--lifespan of each customer
select customer_id, (date(max(invoice_date))-date(min(invoice_date))) as Lifespan_in_days
from online_retail
group by customer_id;

--average order value of each customer
select customer_id, round(sum(price*quantity)/count(distinct invoice),2) as avg_order_value
from online_retail
group by customer_id;

--highest average order value customer
select customer_id, round(sum(price*quantity)/count(distinct invoice),2) as avg_order_value
from online_retail
group by customer_id
order by avg_order_value desc
limit 10;

--frequent buyers
select customer_id, count(distinct invoice) as total_orders
from online_retail
group by customer_id
having count(distinct invoice)>10;

--one-time buyers
select customer_id, count(distinct invoice) as total_orders
from online_retail
group by customer_id
having count(distinct invoice)=1;

--contribution by each customer in total revenue
select customer_id,sum(price*quantity) as revenue, round(sum(price*quantity)*100/sum(sum(price*quantity))over(),2) as revenue_contribution
from online_retail
group by customer_id
order by revenue_contribution desc;
