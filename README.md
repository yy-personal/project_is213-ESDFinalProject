# ESD_Project

Prerequisite

Run up WAMPSERVER
Start up DOCKER 

Scenario 1:

Scenario 2: Fulfill Delivery Order

1) Navigate to Docker Fulfill Delivery Folder

2) Run docker compose up in terminal

3) Open up shippings.html, observe the changes when clicking the various buttons (e.g. accepted/completed/failed)

Scenario 3: Refund Order

1) Import SQL on MySQL

order2.sql
orderRefund.sql
keyboards.sql

2) Navigate to KeyboardUI_Only

3) Open 4 cmd terminal,

python order.py
python inventory.py
python orderRefund.py
python refund_order.py

4) Open up RefundOrder.html with your local host