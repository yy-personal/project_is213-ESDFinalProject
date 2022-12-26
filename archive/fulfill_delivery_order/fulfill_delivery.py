from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from soupsieve import select
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

order_URL = "http://localhost:5012/order"
shipping_record_URL = "http://localhost:5010/shippingrecord"

# Route 1 - Update Shipping Record's reqStatus to Accepted
@app.route("/update_accepted", methods=['POST'])
def update_accepted():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            selected_delivery = request.get_json()['each_shipping_record']
            print("\nReceived a selected delivery in JSON:", selected_delivery)

            # Doing the actual work
            # Send selected delivery info for processing
            result = fulfill_delivery_order(selected_delivery)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "fulfill_delivery.py internal error: " + ex_str
            }), 500

    # If reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# This function invokes shipping microservice for the update_accepted route 
def fulfill_delivery_order(selected_delivery):

    # Invoke shipping_record microservice to update reqStatus
    print('\n-----Invoking shipping_record microservice-----')

    record_ID = selected_delivery["recordID"] # Depending on how selected_delivery looks, navigate to record ID
    new_shipping_record_URL = shipping_record_URL + "/" + str(record_ID) + "/" + "accepted" # Add record ID & status (accepted) to the base URL
    update_shipping_result = invoke_http(new_shipping_record_URL, method='PUT', json=None)
    print('update_shipping_result:', update_shipping_result)

    return {
        "code": 201,
        "data": {
            "update_shipping_result": update_shipping_result,
        }
    }

#------------------------------------------------------------------------------------------------------------------

# Route 2  - Update Shipping Record's reqStatus to Completed & Update Order's Fulfillment Status to Fulfilled
@app.route("/update_completed", methods=['POST'])
def update_completed():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            selected_delivery = request.get_json()['each_shipping_record']
            print("\nReceived a selected delivery in JSON:", selected_delivery)

            # Doing the actual work
            # Send selected delivery info for processing
            result = fulfill_delivery_order2(selected_delivery)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "fulfill_delivery.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# This function invokes both shipping microservice & order microservice for the update_completed route
def fulfill_delivery_order2(selected_delivery):

    # Invoke shipping_record microservice to update reqStatus 
    print('\n-----Invoking shipping_record microservice-----')

    record_ID = selected_delivery["recordID"] # Depending on how selected_delivery looks, navigate to record ID
    new_shipping_record_URL = shipping_record_URL + "/" + str(record_ID) + "/" + "completed" # Add record ID & status (completed) to the base URL
    update_shipping_result = invoke_http(new_shipping_record_URL, method='PUT', json=None)
    print('update_shipping_result:', update_shipping_result)


    # Invoke order microservice to update fulfillment status
    print('\n-----Invoking order microservice-----')

    order_ID = selected_delivery["orderID"] # Depending on how selected_delivery looks, navigate to order ID
    new_order_URL = order_URL + "/" + str(order_ID) # Add order ID to the base URL
    update_order_result = invoke_http(new_order_URL, method='PUT', json=None)
    print('update_order_result:', update_order_result)

    return {
        "code": 201,
        "data": {
            "update_shipping_result": update_shipping_result,
            "update_order_result": update_order_result
        }
    }

#------------------------------------------------------------------------------------------------------------------

# Route 3 - Update Shipping Record's reqStatus to Failed & Send SMS to Customer (Failed Delivery)
@app.route("/update_failed", methods=['POST'])
def update_failed():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            selected_delivery = request.get_json()['each_shipping_record']
            print("\nReceived a selected delivery in JSON:", selected_delivery)

            # Doing the actual work
            # Send selected delivery info for processing
            result = fulfill_delivery_order3(selected_delivery)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "fulfill_delivery.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# This function invokes shipping_record microservice & sms microservice for update_failed route
def fulfill_delivery_order3(selected_delivery):

    # Invoke shipping_record microservice
    print('\n-----Invoking shipping_record microservice-----')

    record_ID = selected_delivery["recordID"] # Depending on how selected_delivery looks, navigate to record ID
    new_shipping_record_URL = shipping_record_URL + "/" + str(record_ID) + "/" + "failed" # Add record ID & status (failed) to the base URL
    update_shipping_result = invoke_http(new_shipping_record_URL, method='PUT', json=None)
    print('update_shipping_result:', update_shipping_result)


    # Invoke SMS microservice to send message to customer
    print('\n\n-----Invoking SMS microservice as order fails-----')
    print('\n\n-----Publishing the message with routing_key=order.error-----')

    message = "Order delivery failed, please contact Keebsforus helpdesk to reshedule your delivery date. Thank you"
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    # make message persistent within the matching queues until it is received by some receiver 
    # (the matching queues have to exist and be durable and bound to the exchange)

    return {
        "code": 201,
        "data": {
            "update_shipping_result": update_shipping_result
        },
        "message": "Shipping failure sent for error handling."
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
