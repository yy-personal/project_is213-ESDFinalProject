import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer , primary_key = True)
    customer_id = db.Column(db.String(30) , nullable = False)
    phone = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String(100) , nullable = False)
    status = db.Column(db.String(10), nullable=False)
    created = db.Column(db.DateTime, nullable = False, default = datetime.now)
    fulfill_status = db.Column(db.String(12) , nullable = False)

    def json(self):
        dto = {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'phone': self.phone,
            'address': self.address,
            'status': self.status,
            'created': self.created,
            'fulfill_status': self.fulfill_status
        }


        dto['order_item'] = []
        for oi in self.order_item:
            dto['order_item'].append(oi.json()
            )
        return dto
    
class Order_Item(db.Model):
    __tablename__ = 'order_item'

    item_id = db.Column(db.Integer , primary_key = True)
    
    order_id = db.Column(db.ForeignKey(
        'order.order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    
    item_name = db.Column(db.String(100) , nullable = False)
    quantity = db.Column(db.Integer , nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    refund_status = db.Column(db.String(10), nullable = False)
    photo_url = db.Column(db.String(64), nullable=False)

    order = db.relationship(
        'Order', primaryjoin='Order_Item.order_id == Order.order_id', backref='order_item')

    def json(self):
        return {'item_id': self.item_id, 'item_name': self.item_name, 'quantity': self.quantity, "price": self.price,'order_id': self.order_id,
        'refund_status': self.refund_status, "photo_url":self.photo_url}


#GET ALL ORDERS
@app.route("/order")
def get_all():
    orderlist = Order.query.all()
    if len(orderlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404

#GET ONE ORDER
@app.route("/order/<string:order_id>")
def find_by_order_id(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "order_id": order_id
            },
            "message": "Order not found."
        }
    ), 404

#CREATE ORDER (POST)
@app.route("/order", methods=['POST'])
def create_order():
    customer_id = request.json.get('customer_id')
    #print(customer_id)

    order = Order(customer_id=customer_id, status='CART')

    cart_item = request.json.get('order_item')

    for item in cart_item:
        order.order_item.append(Order_Item(
            photo_url=item['photo_url'], item_id = item['itemID'],
            item_name=item['itemName'], quantity=item['quantity'], price = item['price']))

    print(request.json['customer_id'])

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500
    
    print(json.dumps(order.json(), default=str)) # convert a JSON object to a string and print

    return jsonify(
        {
            "code": 201,
            "data": order.json()
        }
    ), 201

#UPDATE ORDER
@app.route("/order/<string:order_id>", methods=['PUT'])
def update_order(order_id):
    try:
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "order_id": order_id
                    },
                    "message": "Order not found."
                }
            ), 404

        # update status
        order.fulfill_status = 'FULFILLED'
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order_id": order_id
                },
                "message": "An error occurred while updating the order. " + str(e)
            }
        ), 500

@app.route("/order/refund/<string:order_id>", methods=['PUT'])
def update_refund_order(order_id):
    try:
        orderlist = Order_Item.query.all()
        data = request.get_json()
        for check in orderlist:
            if int(data['orderID']) == int(check.order_id):
                if int(data['itemID']) == int(check.item_id):
                    order = check
        
        #order = Order_Item.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "order_id": order_id
                    },
                    "message": "Order not found."
                }
            ), 404

        # update status
        order.refund_status = 'REFUNDED'
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order_id": order_id
                },
                "message": "An error occurred while updating the order. " + str(e)
            }
        ), 500

@app.route("/order/<string:order_id>", methods=['PATCH'])
def update_specific_order(order_id):
    try:
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "order_id": order_id
                    },
                    "message": "Order not found."
                }
            ), 404

        # update specific thing
        data = order.json()
        order_item = data['order_item']


        order.refund_status = 'REFUNDED'
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order_id": order_id
                },
                "message": "An error occurred while updating the order. " + str(e)
            }
        ), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)
