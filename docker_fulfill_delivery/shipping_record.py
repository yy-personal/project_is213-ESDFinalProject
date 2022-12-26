from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/shipping_record'

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:3306/shipping_record'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)



db = SQLAlchemy(app)

CORS(app)

class ShippingRecord(db.Model):
    __tablename__ = 'shipping_record'

    recordID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    customerID = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    orderID = db.Column(db.Integer, nullable=False)
    reqStatus = db.Column(db.String(64), nullable=False)

    def __init__(self, customerID, address, phone, orderID, reqStatus):
        self.customerID = customerID
        self.address = address
        self.phone = phone
        self.orderID = orderID
        self.reqStatus = reqStatus

    def json(self):
        return {"recordID": self.recordID, "customerID": self.customerID, "address": self.address, "phone": self.phone, "orderID": self.orderID, "reqStatus": self.reqStatus}

# this route will get all shipping records in the database
@app.route("/shippingrecord")
def get_all():
    shippingRecordList = ShippingRecord.query.all()
    if len(shippingRecordList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shippingRecords": [shippingRecord.json() for shippingRecord in shippingRecordList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no shipping records."
        }
    ), 404

#this route to get a specific shipping record using recordID(needed for the website)
@app.route("/shippingrecord/<string:recordID>")
def find_by_recordID(recordID):
    shippingRecordList = ShippingRecord.query.filter_by(recordID=recordID).first()
    if shippingRecordList:
        return jsonify(
            {
                "code": 200,
                "data": shippingRecordList.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "recordID": recordID
            },
            "message": "Order not found."
        }
    ), 404

# this route will get all shipping records in the database based on reqStatus (e.g. accepted)
# 4 different reqStatus: unaccepted, accepted, completed or failed
# e.g. /shippingrecord/unaccepted will return a list of unaccepted shipping records
# yy note: added reqStatus/ to deconflict with other find_by_xx
@app.route("/shippingrecord/reqStatus/<string:reqStatus>")
def find_by_reqStatus(reqStatus):
    shippingRecordList = ShippingRecord.query.filter_by(reqStatus=reqStatus).all()
    if len(shippingRecordList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shippingRecords": [shippingRecord.json() for shippingRecord in shippingRecordList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no matching shipping records."
        }
    ), 404

# this route will update a particular shipping record's reqStatus field in the database based on record ID and the given reqStatus (e.g. accepted)
@app.route("/shippingrecord/<int:recordID>/<string:reqStatus>", methods=['PUT'])
def update_record(recordID, reqStatus):
    shippingRecord = ShippingRecord.query.filter_by(recordID=recordID).first()
    if shippingRecord:
        shippingRecord.reqStatus = reqStatus
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": shippingRecord.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "data": {
                "recordID": recordID
            },
            "message": "Shipping Record not found."
        }
    ), 404    

# this route will create a shipping record
@app.route("/shippingrecord/create", methods=['POST'])
def create_shippingrecord():
    data = request.get_json()
    print(data)
    shippingRecord = ShippingRecord(**data)
    print(shippingRecord)

    try:
        db.session.add(shippingRecord)
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
            "data": shippingRecord.json()
        }
    ), 201
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)