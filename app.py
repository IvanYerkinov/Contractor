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

items.insert_one({"name": "test1", "price": 0, "img_url": "https://m.media-amazon.com/images/M/MV5BMGZmNGIxMTYtMmVjMy00YzhkLWIyOTktNTExZGFiYjNiNzdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg"})
items.insert_one({"name": "test2", "price": 0, "img_url": "https://vignette.wikia.nocookie.net/ghostbusters/images/8/8d/GhostbustersIIStorybookByScholasticSc01.png/revision/latest?cb=20170222172348"})
items.insert_one({'name': 'test3', 'price': 0, 'img_url': ''})


@app.route("/")
@app.route("/", methods=["POST"])
def base():
    return render_template('store.html', items=items.find())

    
@app.route('/cart')
@app.route('/cart/<item_id>', methods=["POST"])
def cart(item_id):
    mycart.insert_one(items.find_one({'_id': ObjectId(item_id)}))
    return render_template('checkout.html', cart=mycart.find())


@app.route('/show/<item_id>', methods=["POST"])
def show(item_id):
    it = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item.html', item=it)
