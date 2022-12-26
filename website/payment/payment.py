#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
import json
import os
import stripe

# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
stripe.api_key = 'sk_test_Ou1w6LVt3zmVipDVJsvMeQsc'

from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='sgd',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret'],
            'created': intent['created'],    #epoch timestamp
            'paymentStatus': intent['status']
        })

    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(port="5030", debug=True)