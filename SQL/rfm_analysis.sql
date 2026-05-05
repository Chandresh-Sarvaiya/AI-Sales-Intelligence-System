select * from online_retail;

select max(invoice_date) from online_retail;


--rfm

create table rfm_segmentation as 
with rfm as (
select customer_id,max(invoice_date) as last_purchase, count(distinct invoice) as frequency, sum(price*quantity) as monetary
from online_retail
group by customer_id
),
time_stamp_to_days as(
select customer_id, date_part('day',max(last_purchase) over()-last_purchase)as recency, frequency,monetary
from rfm
),
rfm_calcuation as(
select customer_id,recency,frequency,monetary,ntile(5) over(order by recency desc) as r_score,ntile(5) over(order by frequency) as f_score, 
ntile(5) over(order by monetary)as m_score
from time_stamp_to_days
)
select customer_id,recency,frequency,monetary, cast(r_score as text)||cast(f_score as text)||cast(m_score as text) as rfm_segment,
case when r_score>=4 and f_score>=4 then 'Champions'
when r_score>=3 and f_score>=3 then 'Loyal Customer'
when r_score>=3 and f_score<=2 then 'Potential Customer'
when r_score<=2 and f_score>=3 then 'At Risk'
when r_score<=2 and f_score<=2 then 'Lost Customer'
end as customer_segment
from rfm_calcuation;



select customer_segment, count(*) as customers
from(
with rfm as (
select customer_id,max(invoice_date) as last_purchase, count(distinct invoice) as frequency, sum(price*quantity) as monetary
from online_retail
group by customer_id
),
time_stamp_to_days as(
select customer_id, date_part('day',max(last_purchase) over()-last_purchase)as recency, frequency,monetary
from rfm
),
rfm_calcuation as(
select customer_id,recency,frequency,monetary,ntile(5) over(order by recency desc) as r_score,ntile(5) over(order by frequency) as f_score, 
ntile(5) over(order by monetary)as m_score
from time_stamp_to_days
)
select customer_id,recency,frequency,monetary, cast(r_score as text)||cast(f_score as text)||cast(m_score as text) as rfm_segment,
case when r_score>=4 and f_score>=4 then 'Champions'
when r_score>=3 and f_score>=3 then 'Loyal Customer'
when r_score>=3 and f_score<=2 then 'Potential Customer'
when r_score<=2 and f_score>=3 then 'At Risk'
when r_score<=2 and f_score<=2 then 'Lost Customer'
end as customer_segment
from rfm_calcuation
order by rfm_segment desc)
group by customer_segment
order by customers desc;

select * from rfm_segmentation;