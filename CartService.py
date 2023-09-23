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

BASE_URL = "http://127.0.0.1:8001"

carts = {  1: [
        {
            "productName": "Apples",
            "quantity": 3,
            "totalPrice": 9.0  
        },
        {
            "productName": "Chips",
            "quantity": 2,
            "totalPrice": 5.0  
        }
    ] }

# def get_products():
#     response = requests.get(f'{BASE_URL}/products')
#     data = response.json().get("product")
#     return data

def get_product(product_id):
    response = requests.get(f'{BASE_URL}/products/{product_id}')
    data = response.json().get("product")
    return data

# Endpoint 1: Get a user's cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_user_cart(user_id):
    if user_id in carts :
        return jsonify({"user's cart": carts[user_id]})
    else:
        return jsonify({"error": "No cart associated with this userID"}), 404
    
def get_user_cart_contents(user_id):
    user_cart = carts.get(user_id, []) # makes a new cart if there is no cart already available
    cart_contents = []
    for in_cart in user_cart:
        in_cart_item = {
               "productName": in_cart["productName"],
               "quantity": in_cart["quantity"],
               "totalPrice": in_cart["totalPrice"]
        }
        cart_contents.append(in_cart_item)
    return cart_contents

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = request.json
    if "quantity" not in data:
        return jsonify({"error": "quantity is required"}), 404
    quantity = request.json.get('quantity')
    quantity_data = {"quantity": quantity}
    product_info = get_product(product_id)
    if product_info is not None:
        if product_info["quantity"] >= quantity:
            user_cart = get_user_cart_contents(user_id)  
            for in_cart in user_cart:
                if in_cart["productName"] == product_info["name"]:
                        in_cart["quantity"] += request.json.get('quantity')
                        in_cart["totalPrice"] = in_cart["quantity"] * product_info["price"]
                        requests.post(f'{BASE_URL}/products/remove/{product_id}', json=quantity_data)
                        carts[user_id] = user_cart
                        return jsonify({"message": "User's cart updated", "user's cart": user_cart}), 201
            user_cart.append({
                    "productName": product_info["name"],
                    "quantity": quantity,
                    "totalPrice": quantity * product_info["price"]
            })
            carts[user_id] = user_cart
            return jsonify({"message": "Product added to  user's cart", "user's cart": user_cart}), 201
        else:
                return jsonify({"error": "Not enough quantity of this product in warehouse"}), 404
    else :
         return jsonify({"error": "Product not found"}), 404  


@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    data = request.json
    if "quantity" not in data:
        return jsonify({"error": "quantity is required"}), 404
    product_info = get_product(product_id)
    if user_id in carts:
        if product_info is not None:
                user_cart = get_user_cart_contents(user_id)
                for in_cart in user_cart:
                    if in_cart["productName"] == product_info["name"]:
                        in_cart["quantity"] -= request.json.get('quantity')
                        in_cart["totalPrice"] = in_cart["quantity"] * product_info["price"]
                        if in_cart["quantity"] <= 0:
                            user_cart.remove(in_cart)
                        carts[user_id] = user_cart
                        return jsonify({"message": "User's cart updated after removal", "cart": user_cart}), 201
                return jsonify({"error": "Product not found in user's cart"}), 404
        else:
            return jsonify({"error": "Product not found"}), 404
    else:
         return jsonify({"error": "No cart associated with this userID"})   

        

if __name__ == '__main__':
    app.run(debug=True)



# def add_to_cart(user_id, product_id):
#     products_response = get_products()
#     for product in products_response:
#             if product["id"] == product_id:
#                 added = product
#                 break
#     if added in carts[user_id]:
#         cart = get_user_cart(user_id)
           
#         product_updated = {
#           #      "name": added["name"],
#                 "quantity": request.json.get("quantity") + request.json.get("quantity"),
#                 "total_price": added["price"] * request.json.get("quantity")
#             }  
#         cart.append(product_added)
#         carts[user_id] = cart
#         return jsonify({"message": "Added product to cart", "user_id": user_id, "cart": cart})
#     else:
#                 cart = carts.get(user_id, [])
           
#         product_added = {
#           #      "name": added["name"],
#                 "quantity": request.json.get("quantity") + request.json.get("quantity"),
#                 "total_price": added["price"] * request.json.get("quantity")
#             }  
#         cart.append(product_added)
#         carts[user_id] = cart
#         return jsonify({"message": "Added product to cart", "user_id": user_id, "cart": cart})
#         return jsonify({"error": "No product found"}), 404

    #  # Default to 1 if quantity is not specified in the request



# @app.route('/cart/<int:user_id>', methods=['GET'])
# def get_user_cart(user_id):
#     for cart in carts :
#          if cart["userID"] == user_id:
#                 return jsonify({"userID": user_id, "cart": cart})
#          else:
#             return jsonify({"error: No cart associated with this userID"}), 404




    # quantity = request.json.get('quantity')
    # product_info = get_product(product_id)
    # if product_info is not None:
    #         user_cart = get_cart_contents(user_id)
    #         for in_cart in user_cart:
    #             if in_cart["productName"] == product_info["name"]:
    #                 in_cart["quantity"] -= quantity
    #                 in_cart["totalPrice"] = in_cart["quantity"] * product_info["price"]
    #                 if in_cart["quantity"] == 0:
    #                     user_cart.remove(in_cart)
    #                 carts[user_id] = user_cart
    #                 return jsonify({"message": "User's cart updated after removal", "cart": user_cart}), 201
    #             else:
    #                 return jsonify({"error": "Product not found in user's cart"}), 404
    # else:
    #     return jsonify({"error": "Product not found in warehouse"}), 404
