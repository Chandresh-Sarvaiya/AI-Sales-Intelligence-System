create table customer_rfm_leadscore (
    customer_id float,
    recency int,
    frequency int,
    monetary decimal(12,2),
    r_score int,
    f_score int,
    m_score int,
    rfm_score int,
    segment varchar(50),
    avgordervalue decimal(12,6),
    purchaseintensity decimal(12,6),
    productdiversity int,
    customer_active_days int,
    email_click_rate decimal(5,2),
    website_visits int,
    time_on_site int,
    discount_response int,
    leadscore decimal(12,6),
    leadscore_log decimal(12,6),
    leadscore_final decimal(12,6)
);

drop table customer_rfm_leadscore;
copy customer_rfm_leadscore from 'E:/SEM 8/Sales_Intelligence_System/Code_Implementation/lead_scoring_online_retail/lead_scoring_final.csv'
delimiter ',' csv header;