--product generating the highest revenue
select product, sum(price*quantity) as revenue
from online_retail
group by product
order by revenue desc
limit 10;

--total revenue distributed across different customer revenue segments
with customer_revenue as (
select customer_id, sum(price*quantity) as revenue
from online_retail
group by customer_id
),
ranked_customers as (
select customer_id, revenue,ntile(5) over(order by revenue desc) as revenue_grp
from customer_revenue
)
select revenue_grp, sum(revenue) as grp_revenue, round(sum(revenue)*100/sum(sum(revenue)) over(),2) as revenue_percentage
from ranked_customers
group by revenue_grp;

--ranking of customers based on their revenue
select customer_id,sum(price*quantity) as revenue, rank() over (order by sum(price*quantity) desc) as revenue_rank
from online_retail 
group by customer_id;

--percentage of revenue contributed by each customer
select customer_id,sum(price*quantity) as revenue, round(sum(price*quantity)*100/sum(sum(price*quantity)) over(),2) as revenue_contribution
from online_retail
group by customer_id
order by revenue_contribution desc;

--time interval of each customer between consecutive purchase
select distinct customer_id,invoice_date,lag(invoice_date) over(partition by customer_id order by invoice_date) as previous_purchase,
invoice_date-lag(invoice_date) over(partition by customer_id order by invoice_date) as purchase_interval
from online_retail
group by invoice_date,customer_id
order by customer_id,invoice_date;

--revenue contribution and rank of each product
with product_revenue as (
select stock_code,product, sum(price*quantity) as revenue
from online_retail
group by stock_code,product
)
select stock_code,product,revenue,rank() over(order by revenue desc) as product_rank, round(revenue*100/sum(revenue) over(),2) as revenue_percentage
from product_revenue
order by product_rank;