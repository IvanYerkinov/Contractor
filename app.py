from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=host)
db = client.Contractor
items = db.items
mycart = db.cart

app = Flask(__name__)

items.drop()
mycart.drop()

item = {"name": "", "price": 0, "img_url": ""}

items.insert_one({"name": "Con Air", "price": 9.99, "img_url": "https://m.media-amazon.com/images/M/MV5BMGZmNGIxMTYtMmVjMy00YzhkLWIyOTktNTExZGFiYjNiNzdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg"})
items.insert_one({"name": "Double Down", "price": 9.99, "img_url": "https://horrornews.net/wp-content/uploads/2017/12/Double-Down-2005-movie-Neil-Breen-4.jpg"})
items.insert_one({'name': 'Manos the Hands of Fate', 'price': 9.99, 'img_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Manosposter.jpg/220px-Manosposter.jpg'})
items.insert_one({'name': 'The Room', 'price': 9.99, 'img_url': 'https://images.gowatchit.com/posters/original/THE_ROOM.jpg'})


def getPrice():
    price = 0
    listofcart = mycart.find()
    for index in listofcart:
        price += index['price']
    return price


@app.route("/")
@app.route("/", methods=["POST"])
def base():
    return render_template('store.html', items=items.find())


@app.route('/cart', methods=["POST"])
def showcart():
    return render_template('checkout.html', mcart=mycart.find(), var=getPrice())


@app.route('/cart/<item_id>', methods=["POST"])
def cart(item_id):
    object = items.find_one({'_id': ObjectId(item_id)})

    object["_id"] = ObjectId()

    mycart.insert_one(object)
    return render_template('checkout.html', mcart=mycart.find(), var=getPrice())


@app.route('/remcart/<item_id>', methods=["POST"])
def remcart(item_id):
    mycart.delete_one({'_id': ObjectId(item_id)})
    return render_template('checkout.html', mcart=mycart.find(), var=getPrice())


@app.route('/emptycart', methods=["POST"])
def empcart():
    mycart.drop()
    return render_template('checkout.html', mcart=mycart.find(), var=getPrice())


@app.route('/show/<item_id>', methods=["POST"])
def show(item_id):
    it = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item.html', item=it)
