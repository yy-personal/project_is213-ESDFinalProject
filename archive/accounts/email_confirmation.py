import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import sendgrid
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

import json

app = Flask(__name__)
CORS(app)

@app.route("/emailconfirmation", methods=["POST"])
def emailconfirmation():
    if request.is_json:
        try:
            getOrder = request.get_json()
            print("Recieved a email request in", type(getOrder), getOrder)
            email_request = getOrder
            # extract json content from request
            TO_EMAILS = email_request['email']
            FROM_EMAIL = "ycwang.2020@scis.smu.edu.sg"
            Sender_Name = email_request['Name']
            dateTime = email_request['DateTime']
            transaction_id = email_request['TransactionID']
            shipping_address = email_request['shippingAddress']


            subject = "Confirmation of Order ID: " + transaction_id
            APIKEY = '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'
            TEMPID = 'd-8998ea72c76f40fd9592b188ac3c9899'
            message = Mail(
                from_email=FROM_EMAIL,
                subject=subject,
                to_emails=TO_EMAILS)
            # pass custom values for our HTML placeholders
            message.dynamic_template_data = {
                'Sender_Name': Sender_Name,
                'dateTime': dateTime,
                'shipping_address': shipping_address,
                'transaction_id':transaction_id

            }
            message.template_id = TEMPID
            # create our sendgrid client object, pass it our key, then send and return our response objects
            try:
                # os.environ.get('SENDGRID_API_KEY') <-- ideally 
                sg = SendGridAPIClient(APIKEY)
                response = sg.send(message)
                code, body, headers = response.status_code, response.body, response.headers
                print(f"Response code: {code}")
                print(f"Response headers: {headers}")
                print(f"Response body: {body}")
                print("Dynamic Messages Sent!")
            except Exception as e:
                print("Error: {0}".format(e))
            
                        
            return jsonify({
                "code": 200,
                "message": "Email sent successfully."
            }), 200

        except Exception as e:
            print(type(e))
            return str(e)



if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for sending an email...")
    app.run(host="0.0.0.0", port=5012, debug=True)