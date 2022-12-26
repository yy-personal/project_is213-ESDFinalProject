from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/orderRefund'
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)

CORS(app)

class OrderRefund(db.Model):
    __tablename__ = 'orderRefund'

    refundID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    customerID = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    orderID = db.Column(db.Integer, nullable=False)
    itemID = db.Column(db.Integer, nullable=False)


    def __init__(self, customerID, address, phone, orderID, itemID):
        self.customerID = customerID
        self.address = address
        self.phone = phone
        self.orderID = orderID
        self.itemID = itemID

    def json(self):
        return {"refundID": self.refundID, "customerID": self.customerID, "address": self.address, "phone": self.phone, "orderID": self.orderID, "itemID": self.itemID}

# this route will get all shipping records in the database
@app.route("/orderRefund")
def get_all():
    refundList = OrderRefund.query.all()
    if len(refundList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "refundList": [refundRecord.json() for refundRecord in refundList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no refund shipping records."
        }
    ), 404

#this route to get a specific order using recordID(needed for the website)
@app.route("/orderRefund/<string:refundID>")
def find_by_refundID(refundID):
    refundList = OrderRefund.query.filter_by(refundID=refundID).first()
    if refundList:
        return jsonify(
            {
                "code": 200,
                "data": refundList.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "refundID": refundID
            },
            "message": "RefundID not found."
        }
    ), 404

#not used as of now but perhaps future implementaion
# this route will update a particular shipping record's reqStatus field in the database based on record ID and the given reqStatus (e.g. accepted)
@app.route("/orderRefund/<int:refundID>", methods=['PUT'])
def update_record(refundID):
    refundShipping = OrderRefund.query.filter_by(refundID=refundID).first()
    if refundShipping:
        refundShipping.refundID = refundID
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": refundShipping.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "data": {
                "refundID": refundID
            },
            "message": "Refund Shipping Record not found."
        }
    ), 404    

# this route will create a shipping record
@app.route("/orderRefund/create", methods=['POST'])
def create_refundShipping():
    data = request.get_json()
    print(data)
    refundShipping = OrderRefund(**data)
    print(refundShipping)

    try:
        db.session.add(refundShipping)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                },
                "message": "An error occurred creating the shipping record."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": refundShipping.json()
        }
    ), 201
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5014, debug=True)