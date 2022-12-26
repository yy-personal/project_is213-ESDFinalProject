from xml.dom.minidom import TypeInfo
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

order_URL = "http://localhost:5012/order"
shipping_record_URL = "http://localhost:5014/orderRefund"

@app.route("/refund_order", methods=['POST'])
def get_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)
            print(order)
            # do the actual work
            # 1. Send order info {cart items}
            result = processRefundOrder(order)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "refund_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processRefundOrder(order):

    print('\n-----Invoking order microservice-----')
    print('-order-')
    print(order)
    print('-order-')

    order_URL = "http://localhost:5012/order"
    orderid = order["orderID"]
    itemid = order['itemID']
    order_URL = order_URL + "/" + str(orderid)
    order_result = invoke_http(order_URL, method='GET')
    code = order_result["code"]

    if code not in range(200, 300):

        #Return error
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Order creation failure asdasd"
        }
    
    print('\n-----Invoking inventory microservice-----')
    inventory_URL = "http://localhost:5013/inventory"
    inventory_result = invoke_http(inventory_URL, method='GET')
    itemIndex = -1

    #inventory check and deduction
    for inventory in inventory_result['data']['keyboards']:
        itemIndex += 1
        if int(inventory['itemID']) == int(itemid):
            if inventory['quantity'] > 0:
                print('inventory before deduct')
                print(inventory)
                update_url = inventory_URL + "/" + str(itemid)
                updateData = inventory
                updateData['quantity'] = int(inventory['quantity']) - 1
                inventory_result = invoke_http(
                update_url, method="PUT", json=updateData)
                print('inventory after deduct', inventory_result)
            else:
                return {
                    "code": 400,
                    "data": {
                    "order_result": order_result
                        },
                    "message": str(inventory_result['data']['keyboards'][itemIndex]['itemName']) + " is not instock currently, please try again!"
                        }

    
    # Send refund order to shipping
    # Invoke the shipping record microservice
    print('\n\n-----Invoking shipping_record microservice-----')    
    
    #setting variables to send
    customerid = order_result['data']['customer_id']
    address = order_result['data']['address']
    phone = order_result['data']['phone']
    orderid = order_result['data']['order_id']
    itemID = itemid
    #send variables
    shippingData = {
        "customerID": customerid,
        "address": address,
        "phone": phone,
        "orderID": orderid,
        "itemID": itemID,
    }

    #print(shippingData)

    shipping_create_URL ="http://localhost:5014/orderRefund/create"
    shipping_create_result = invoke_http(
        shipping_create_URL, method="POST", json=shippingData)

    print('--=-=- shipping created')
    print(shipping_create_result)
    print('--=-=- shipping created')

    #update order_item refund status
    updateorderData = {
        "orderID": orderid,
        "itemID": itemID,
    }
    update_order_url = 'http://localhost:5012/order/refund/' + str(orderid)
    update_result = invoke_http(
                update_order_url, method="PUT", json=updateorderData)
    print(update_result)

    # Check the shipping result if its failure
    code = shipping_create_result["code"]
    if code not in range(200, 300):
        
        #Return error
        return {
            "code": 400,
            "data": {
                "order_result": order_result,
                "shipping_result": shipping_create_result
            },
            "message": "Shipping record error sent for error handling."
        }

    # 7. Everything success, Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "order_result": order_result,
            "shipping_result": shipping_create_result
        }
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5101, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
