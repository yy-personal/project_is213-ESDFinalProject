from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

#run below statement in terminal
#set dbURL=mysql+mysqlconnector://root@localhost:3306/keyboards
#python keyboard.py

#run with docker
#docker build -t <dockerid>/keyboard:1.0
#docker build . -f keyboard.Dockerfile -t keyboard
#docker run --rm -it helloworld

#docker dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/keyboards <dockerid>/keyboard:1.0	
#docker run -p 5000:5000 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/book <dockerid>/keyboard:1.0


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:3306/keyboards'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/keyboards'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Keyboard(db.Model):
    __tablename__ = 'keyboards'

    itemID = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String(64), nullable=False)
    photo_url = db.Column(db.String(64), nullable=False)


    def __init__(self, itemID, itemName, price, quantity, category, photo_url):
        self.itemID = itemID
        self.itemName = itemName
        self.price = price
        self.quantity = quantity
        self.photo_url = photo_url
        self.category = category



    def json(self):
        return {"itemID": self.itemID, "itemName": self.itemName, "price": self.price, "quantity": self.quantity ,"photo_url":self.photo_url, "category":self.category }


@app.route("/inventory")
def get_all():
    keyboardList = Keyboard.query.all()
    if len(keyboardList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "keyboards": [keyboard.json() for keyboard in keyboardList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no keyboards."
        }
    ), 404


@app.route("/inventory/<string:itemID>")
def find_by_itemID(itemID):
    keyboard = Keyboard.query.filter_by(itemID=itemID).first()
    if keyboard:
        return jsonify(
            {
                "code": 200,
                "data": keyboard.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Keyboard not found."
        }
    ), 404


@app.route("/inventory/<string:itemID>", methods=['POST'])
def create_keyboard(itemID):
    if (Keyboard.query.filter_by(itemID=itemID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "itemID": itemID
                },
                "message": "Keyboard already exists."
            }
        ), 400

    data = request.get_json()
    keyboard = Keyboard(itemID, **data)

    try:
        db.session.add(keyboard)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "itemID": itemID
                },
                "message": "An error occurred creating the keyboard."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": keyboard.json()
        }
    ), 201


@app.route("/inventory/<string:itemID>", methods=['PUT'])
def update_keyboard(itemID):
    keyboard = Keyboard.query.filter_by(itemID=itemID).first()
    if keyboard:
        data = request.get_json()
        if data['itemName']:
            keyboard.itemName = data['itemName']
        if data['price']:
            keyboard.price = data['price']
        if data['quantity']:
            keyboard.quantity = data['quantity']
        if data['category']:
            keyboard.category = data['category']
        if data['photo_url']:
            keyboard.photo_url = data['photo_url']

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": keyboard.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "itemID": itemID
            },
            "message": "Keyboard not found."
        }
    ), 404


@app.route("/inventory/<string:itemID>", methods=['DELETE'])
def delete_keyboard(itemID):
    keyboard = Keyboard.query.filter_by(itemID=itemID).first()
    if keyboard:
        db.session.delete(keyboard)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "itemID": itemID
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "itemID": itemID
            },
            "message": "Keyboard not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5013, debug=True)
