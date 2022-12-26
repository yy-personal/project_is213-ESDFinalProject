from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
# from accounts.email_confirmation import emailconfirmation
from invokes import invoke_http
import json

app = Flask(__name__)
CORS(app)

payment_URL = "http://localhost:5030/payment"
order_URL = "http://localhost:5012/order"
# shipping_record_URL = "http://localhost:5019/shipping_record"
# inventory_URL = "http://localhost:5013/inventory"
# #cart_URL = "http://localhost:5014/cart"


@app.route("/place_an_order", methods=['POST'])
def place_order():
    # only trigger the order microservice 
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            ticket = request.get_json() 
            print("\nReceived an order in JSON:", ticket )

            # do the actual work
            # 1. Send payment info 
            result = processPlaceOrder(ticket)
            print (result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_an_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify(
        
    {
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# """ @app.route("/completed_payment", methods=['GET'])
# def completedPayment():


# def emailconfirmation():
#     name = 
#     email = 
#     order_id = 
#     shippingAddresss = 
# """

def processPlaceOrder(cart):
    # invoking order microservice
    # 2. Send the order info
    # Invoke the order microservice
    print('\n-----Invoking order microservice-----')
    # parsing the cart information to the order microservice

    print(cart)
    
    order_json = {
    'itemID' : cart[0].itemID,
    'itemName' : cart[0].itemName,
    'price' : cart[0].price,
    'quantity' : cart[0].quantity
}

    
    order_result = invoke_http(order_URL, method='POST', json=order_json)
    # print the result to the terminal 
    print('order_result:', order_result)


    # Check the order result if creation is successful; if a failure, print onto the console and end the complex microservice 
    code = order_result["code"]
    if code not in range(200, 300):
        return {
                "code": {
                        "order_result": order_result},
                "message": "Order Creation failure"
            }
   
    # 3. send the payments details - amount
    # Invoke the  payment microservices if order creation is successful
    # payment microservice will take in the amount required and the parse it to the payment microservice
    
    
    print('\n-----Invoking payment microservice-----')
    payment_json = {
        'amount' : ticket['amount'], 
        'token' :ticket['paypalToken']
    }

    payment_result = invoke_http(payment_URL, method='POST', json=payment_json)

    # update the payment status 
    print('payment_result:', payment_result) 


    # Check the payment result if creation is successful; if a failure, print onto the console and end the complex microservice 
    code = payment_result["code"]
    if code not in range(200, 300):
        return {
                "code": 500,
                "data": {
                        "payment_result": payment_result,
                        "order_result": order_result},
                    
                "message": "Payment Failure"
            }

    # # 4. Send Updated Inventory
    # # Invoke the inventory record microservice
    # print('\n\n-----Invoking inventory microservice-----')
    # inventory_json = {
    #         'itemID' : new['itemID'], 
    #         'itemInventorQuantity' :new['itemInventoryQuantity']
    #     }

    # inventory_result = invoke_http(
    #     inventory_URL, method="POST", json=inventory_json)
    # print("inventory_result:", inventory_result, '\n')

    #  # Check the inventory result if creation is successful; if a failure, print onto the console and end the complex microservice 
    # code = inventory_result["code"]
    # if code not in range(200, 300):
    #     return {
    #             "code": 500,
    #             "data": {
    #                 "order_result": order_result,
    #                 "payment_result": payment_result,
    #                 "inventory_result": inventory_result,

    #                 },
    #             "message": "Inventory Failure"
    #         }

    # # 5. Send new order to shipping
    # # Invoke the shipping record microservice
    # print('\n\n-----Invoking shipping_record microservice-----')
    # shipping_result = invoke_http(
    #     shipping_record_URL, method="POST", json=order_result['data'])
    # print("shipping_result:", shipping_result, '\n')

    # # Check the shipping result;
    # # if a failure, send it to the error microservice.
    # code = shipping_result["code"]
    # if code not in range(200, 300):
    #     return {
    #             "code": 500,
    #             "data": {"order_results": order_result,
    #                     "payment_result": payment_result,
    #                     "inventory_result": inventory_result,
    #                     "shipping_result": shipping_result}
    #                     ,
    #             "message": "Shipment Creation Failure"
    #         }

    # 7. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "order_result": order_result,
            # "shipping_result": shipping_result,
            "payment_result": payment_result,
            # "inventory_result" : inventory_result       
            }

    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
        " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
