drop table online_retail;

create table online_retail(
	invoice varchar(10),
	stock_code varchar(20),
	product varchar(100),
	quantity integer,
	invoice_date timestamp,
	price numeric(10,2),
	customer_id integer,
	country varchar(20)
)

set datestyle='DMY';


copy online_retail from 'E:/SEM 8/Sales_Intelligence_System/Datasets/Online Retail Dataset/online_retail_I.csv'
delimiter ',' csv header;

copy online_retail from 'E:/SEM 8/Sales_Intelligence_System/Datasets/Online Retail Dataset/online_retail_II.csv'
delimiter ',' csv header;

select * from online_retail;


create table online_retail_backup as
select * from online_retail;

select * from online_retail where quantity<0;
select * from online_retail where price<0;
select * from online_retail where price<0 and quantity<0;

delete from online_retail where quantity<0 or price<0;

select * from online_retail;

select * from online_retail where customer_id is NULL;

delete from online_retail where customer_id is NULL;

select * from online_retail_backup;