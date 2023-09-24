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

BASE_URL = "https://shenoy-product-service.onrender.com"

# BASE_URL = "http://127.0.0.1:8001"

carts = {}


def get_product(product_id):
    response = requests.get(f'{BASE_URL}/products/{product_id}')
    data = response.json().get("product")
    return data

def get_updated_product(quantity, product_id):
    quantity_json = {"quantity": quantity}
    response = requests.post(f'{BASE_URL}/products/remove/{product_id}', json=quantity_json)
    data = response.json().get("updated product")
    return data

# Endpoint 1: Get a user's cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_user_cart(user_id):
    if user_id in carts : # iterate through carts to see if the userid is present and return its contents if found
        return jsonify({"user's cart": carts[user_id]})
    else:
        return jsonify({"error": "No cart associated with this userID"}), 404

 # method to get the contents of a user cart to make it iterable for later usage    
def get_user_cart_contents(user_id):
    user_cart = carts.get(user_id, []) # makes a new cart if there is no cart already available
    cart_contents = [] # new contents array to grab whatever's inside the carts
    for in_cart in user_cart:
        in_cart_item = {
               "productName": in_cart["productName"],
               "quantity": in_cart["quantity"],
               "totalPrice": in_cart["totalPrice"]
        }
        cart_contents.append(in_cart_item) 
    return cart_contents 

# Endpoint 2: Add a product to a cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = request.json
    if "quantity" not in data:
        return jsonify({"error": "quantity is required"}), 404 # check to make sure the quantity is specified in the request body
    quantity = request.json.get('quantity')
    quantity_data = {"quantity": quantity}
    product_info = get_product(product_id) 
    if product_info is None:
        return jsonify({"error": "Product not found"}), 404 # check for valid product ID
    response = requests.post(f'{BASE_URL}/products/decrease/{product_id}', json=quantity_data) # make post call to API to decrease quantity of product in warehouse
    if response.status_code == 200: # if API sends back a success response
        user_cart = get_user_cart_contents(user_id)   
        for in_cart in user_cart:
            if in_cart["productName"] == product_info["name"]: # check if the name of the product associated with its ID, exists in the cart
                        in_cart["quantity"] += quantity # update quantity & total price of the product 
                        in_cart["totalPrice"] = in_cart["quantity"] * product_info["price"]
                        # get_updated_product(quantity, product_id)
                        carts[user_id] = user_cart
                        return jsonify({"message": "User's cart updated", "user's cart": user_cart}), 201
        user_cart.append({ # if the product is not already in the cart, add it to the cart
                    "productName": product_info["name"],
                    "quantity": quantity,
                    "totalPrice": quantity * product_info["price"]
        })
        carts[user_id] = user_cart
        return jsonify({"message": "Product added to  user's cart", "user's cart": user_cart}), 201
    else:
            return jsonify({"error": "Not enough quantity of this product in warehouse"}), 404 # API sends back error

# Endpoint 3: Remove a product from a cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    data = request.json
    if "quantity" not in data:
        return jsonify({"error": "quantity is required"}), 404 # check to make sure the quantity is specified in the request body
    quantity = request.json.get('quantity')
    quantity_data = {"quantity": quantity}
    product_info = get_product(product_id)
    if product_info is None:
         return jsonify({"error": "Product not found"}), 404
    if user_id in carts: # check if there is a user ID associated to the cart
            user_cart = get_user_cart_contents(user_id) # grab contents of the cart
            for in_cart in user_cart: # iterate through user's cart, updating quantity and total prices of items
                if in_cart["productName"] == product_info["name"]:
                    if quantity <= in_cart["quantity"]: # checks if the quantity in request body exceeds quantity in cart
                        requests.post(f'{BASE_URL}/products/increase/{product_id}', json=quantity_data) # makes API call to increase quantity of product in warehouse
                        in_cart["quantity"] -= quantity
                        in_cart["totalPrice"] = in_cart["quantity"] * product_info["price"]
                        if in_cart["quantity"] == 0: # if the quantity of a product reaches 0 remove it from the cart
                            user_cart.remove(in_cart)
                        carts[user_id] = user_cart
                        return jsonify({"message": "User's cart updated after removal", "cart": user_cart}), 201
                    else:
                         return jsonify({"error": "Exceeds quantity in cart"})     
            else:
                return jsonify({"error": "Product not found in user's cart"}), 404
    else:
         return jsonify({"error": "No cart associated with this userID"})   

        

if __name__ == '__main__':
    app.run(debug=True, host='https://shenoy-cart-service.onrender.com')



