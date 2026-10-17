# File: customers.csv

customer_id: INTEGER
full_name: STRING
email: STRING
created_at: DATETIME

# File: order_items.csv

order_item_id: INTEGER
order_id: INTEGER
product_id: INTEGER
quantity: INTEGER
unit_price: DECIMAL(10,2)

# File: orders.csv

order_id: INTEGER
customer_id: INTEGER
order_date: DATE
status: STRING 

# File: products.csv

product_id: INTEGER
product_name: STRING
price: DECIMAL
stock_quantity: INTEGER

