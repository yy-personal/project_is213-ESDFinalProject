Prerequisite

Run up WAMPSERVER
Start up DOCKER 

Import following files to SQL database

keyboards.sql
order2.sql
orderRefund.sql
payments.sql
shipping_record.sql


Scenario 1: Place An Order 
----------------------
run 

- inventory.py 
- payment.py
- order.py

locally to get started 

To get the payment gateway working 

1. Build the server
----------------------
pip install -r requirements.txt


2. Run the payment
----------------------
python payment.py
 
Go to [http://localhost:5030/checkout.html](http://localhost:5030/checkout.html)

To view and add item to the cart





Scenario 2: Fulfill Delivery Order

1) Navigate to Docker Fulfill Delivery Folder

2) Run docker compose up in terminal

3) Open up shippings.html, observe the changes when clicking the various buttons (e.g. accepted/completed/failed)



Scenario 3:
----------------------

1) Navigate to KeyboardUI_Only folder

2) Open 4 cmd terminal,

python order.py
python inventory.py
python orderRefund.py
python refund_order.py

3) Open up RefundOrder.html with your local host