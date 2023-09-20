# Name: Satya Shenoy
# Due Date: 9/24/23
# Program: Assignment-2 Cart Service
# Course: CMSC455
#----------------------------------------------------------------------------------------------------#
# Develop another Flask application named ”Cart Service” serving as the second microservice. Create
# the following endpoints, which interact with the ”Product Service” microservice:
# /cart/{user id} (GET): Retrieve the current contents of a user’s shopping cart, including prod-
# uct names, quantities, and total prices.
# /cart/{user id}/add/{product id} (POST): Add a specified quantity of a product to the user’s cart.
# /cart/{user id}/remove/{product id} (POST): Remove a specified quantity of a product from the
# user’s cart.
#----------------------------------------------------------------------------------------------------#

import os
import requests
from flask import Flask, jsonify, request
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:5000"

carts = {}

def get_products():
    response = requests.get(f'{BASE_URL}/products/')
    data = response.json()
    return data

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_user_cart(user_id):
    user_cart = carts.get(user_id, [])
    return jsonify({"user_id": user_id, "cart": user_cart})


@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    products_response = get_products()
    for product in products_response:
            if product["id"] == product_id:
                added = product
                break
    if added:
        added_quantity = request.json.get("quantity")

        cart = carts.get(user_id, [])
           
        product_added = {
                "product_id": request.json.get["id"],
                "name": added["name"],
                "quantity": added_quantity,
                "total_price": added["price"] * added_quantity
            }  
        cart.append(product_added)
        carts[user_id] = cart

        return jsonify({"message": "Added a product to cart", "user_id": user_id, "cart": cart})
    else:
        return jsonify({"error": "No product found"}), 404



        
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
     fff