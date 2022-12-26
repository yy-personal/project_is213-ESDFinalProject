from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)

# Uncomment below for local
# ===
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/esdproject_accounts'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ===
# Uncomment below for docker
# ===
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
# ===

db = SQLAlchemy(app)
CORS(app)

class accounts(db.Model):
    __tablename__ = 'accounts'

    customer_id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(8), nullable=False)
    points = db.Column(db.Integer)
    


    def __init__(customer_id, name, email, address, phone_number, points):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.points = points


    def json(self):
        return {"customer_id": self.customer_id, "name": self.name, "email": self.email, "address": self.address, "phone_number": self.phone_number, "points": self.points}

@app.route("/accounts")
def get_all():
        accounts_list = accounts.query.all()
        if len(accounts_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "accounts": [accounts.json() for accounts in accounts_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no accounts."
            }
        ), 404

@app.route("/accounts/<string:customer_id>")
def find_by_customer_id(customer_id):
    account = accounts.query.filter_by(customer_id=customer_id).first()
    if account:
        return jsonify(
            {
                "code": 200,
                "data": account.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404



@app.route("/accounts/<string:customer_id>/<int:points>", methods=['PUT'])
def update_account_points(customer_id,points):
    account = accounts.query.filter_by(customer_id=customer_id).first()
    if account:
        account.points = points
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": account.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "customer_id": customer_id
            },
            "message": "Account points not found."
        }
    ), 404

@app.route("/accounts/<string:customer_id>", methods=['PUT'])
def update_account_all(customer_id):
    account = accounts.query.filter_by(customer_id=customer_id).first()
    if account:
        data = request.get_json()
        if data['address']:
            account.address = data['address']
        if data['email']:
            account.email = data['email']
        if data['name']:
            account.name = data['name']
        if data['phone_number']:
            account.phone_number = data['phone_number']
        if data['points']:
            account.points = data['points']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": account.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "customer_id": customer_id
            },
            "message": "Account not found."
        }
    ), 404

@app.route("/accounts/<string:customer_id>", methods=['DELETE'])
def delete_account(customer_id):
    account = accounts.query.filter_by(customer_id=customer_id).first()
    if account:
        db.session.delete(account)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "customer_id": customer_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "customer_id": customer_id
            },
            "message": "Account not found."
        }
    ), 404

@app.route("/accounts/<string:customer_id>", methods=['POST'])
def create_account(customer_id):
        if (accounts.query.filter_by(customer_id=customer_id).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "customer_id": customer_id
                    },
                    "message": "Account already exists."
                }
            ), 400

        data = request.get_json()
        account = accounts(customer_id, **data)

        try:
            db.session.add(account)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "customer_id": customer_id
                    },
                    "message": "An error occurred creating the account."
                }
            ), 500

        return jsonify(
            {
                "code": 201,
                "data": account.json()
            }
        ), 201


# For Docker
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)

# if __name__ == '__main__':
#     app.run(port=5011, debug=True)
