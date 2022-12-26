from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)

# Uncomment below for local
# ===
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/cart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ===
# Uncomment below for docker
# ===
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
# ===

db = SQLAlchemy(app)
CORS(app)

class cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.String(8), primary_key=True)
    items = db.Column(db.String(200), nullable=False)
    


    def __init__(cart_id, items):
        self.cart_id = cart_id
        self.items = items


    def json(self):
        return {"cart_id": self.cart_id, "items": self.items}

@app.route("/cart")
def get_all():
        cart_list = cart.query.all()
        if len(cart_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "accounts": [cart.json() for cart in cart_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no carts."
            }
        ), 404


@app.route("/cart/<string:items>", methods=['PUT'])
def update_account_items(items):
    cart_item = cart.query.filter_by(cart_id=1).first()
    if cart_item:
        cart_item.items = items
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": cart_item.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "cart_id": 1
            },
            "message": "Cart not found."
        }
    ), 404

""" @app.route("/cart/" , methods=['POST'])
def create_cart():
    data = request.get_json()
    cart_data = cart(**data)

    try:
        db.session.add(cart_data)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                },
                "message": "An error occurred creating the cart record."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": cart_data.json()
        }
    ), 201 """


# For Docker
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5011, debug=True)

if __name__ == '__main__':
    app.run(port=5014, debug=True)

