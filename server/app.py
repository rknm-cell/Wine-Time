#!/usr/bin/env python3

# Standard library imports
from flask import Flask, request, make_response, jsonify, session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse

from models import db, User, Product, Cart_Item, Shopping_Session

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)
parser = reqparse.RequestParser()
# Views go here!

class Products(Resource):
    def get(self):
        products_dict = [products.to_dict(only = ("id", "name", "description", "image_url", "price", "units", "units_sold")) for products in Product.query.all()]

        response = make_response(
            products_dict,
            200
        )

        return response

api.add_resource(Products, "/products")

class Cart_Items(Resource):

    def get(self):
        cart_items_dict = [cart_items.to_dict() for cart_items in Cart_Item.query.all()]

        response = make_response(
            cart_items_dict,
            200
        )

        return response

    def post(self):
        
        new_cart_item = Cart_Item(
            product_id = request.json['product_id'],
            shopping_session_id = request.json['shopping_session_id'],
            product_num = request.json['product_num']
        )

        db.session.add(new_cart_item)
        db.session.commit()

        cart_item_dict = new_cart_item.to_dict()
        
        response = make_response(
            cart_item_dict,
            201
        )
        return response
    
    def patch(self, product_id):
        if product_id not in Cart_Item:
            return {'message': 'Product not found'}, 404

        args = parser.parse_args()
        new_product_num = args['product_num']

        # Update the product number
        Cart_Item[product_id]['product_num'] = new_product_num

        return {'message': 'Product updated', 'product': Cart_Item[product_id]}

    
api.add_resource(Cart_Items, '/cart_items')

class Cart_ItemsByID(Resource):
    def get(self, id):
        cartitem = Cart_Item.query.filter_by(id = id).first()

        if cartitem:
            cartitem_dict = cartitem.to_dict()

            response = make_response(
                cartitem_dict,
                200
            )

            return response
        
        return {"error": "Cart item not found"}, 404

    def delete(self, id):

        cartitem = Cart_Item.query.filter_by(id = id).first()

        if cartitem:
            db.session.delete(cartitem)
            db.session.commit()

            response = make_response(
                "",
                204
            )

            return response
        
        return {"error": "Cart item not found"}, 404

api.add_resource(Cart_ItemsByID, '/cart_items/<int:id>')

class Shopping_Sessions(Resource):

    def post(self):
        
        new_shopping_session = Shopping_Session(
            user_id = request.json['user_id'],
        )

        db.session.add(new_shopping_session)
        db.session.commit()

        shopping_session_dict = new_shopping_session.to_dict()
        
        response = make_response(
            shopping_session_dict,
            201
        )
        return response
        
api.add_resource(Shopping_Sessions, '/shopping_sessions')

class Shopping_SessionsByID(Resource):

    def patch(self, id):
        shopping_session = Shopping_Session.query.filter_by(id = id).first()

        for attr in request.json:
            
            setattr(shopping_session, attr, request.json[attr])

        db.session.add(shopping_session)
        db.session.commit()

        shopping_session_dict = shopping_session.to_dict()

        response = make_response(
            shopping_session_dict,
            202
        )

        return response

api.add_resource(Shopping_SessionsByID, '/shopping_sessions/<int:id>')


class Login(Resource):

    def post(self):

        email = request.get_json()['email']
        password = request.get_json()['password']

        user = User.query.filter(User.email == email).first()

        if user.authenticate(password):

            session['user_id'] = user.id
            return user.to_dict(), 200

        return {'error': '401 Unauthorized'}, 401
    
api.add_resource(Login, "/login")

class Signup(Resource):

    def post(self):
        
        email = request.get_json()['email']
        password = request.get_json()['password']
        admin = request.get_json()['admin']

        if email and password:
            
            new_user = User(email=email)
            new_user.password_hash = password
            new_user.admin = admin
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            
            return new_user.to_dict(), 201

        return {'error': '422 Unprocessable Entity'}, 422
    
api.add_resource(Signup, "/signup")

class CheckSession(Resource):

    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return {'message': '401: Not Authorized'}, 401

api.add_resource(CheckSession, '/check_session')

class Logout(Resource):

    def delete(self): # just add this line!
        session['user_id'] = None
        return {'message': '204: No Content'}, 204

api.add_resource(Logout, '/logout')

# class Users(Resource):
#     def get(self):
#         pass
    
# api.add_resource(Users, '/users')


# class UsersById(Resource):
#     def get(self):
#         pass
#     def post(self):
#         pass
#     def patch(self):
#         pass
#     def delete(self):
#         pass
# api.add_resource(UsersById, '/users/<int:id>')


# class User_Products(Resource):
#     def get(self):
#         pass
    
# api.add_resource(User_Products, '/userproducts')

# class Transactions(Resource):
#     def get(self):
#         pass
#     def post(self):
#         pass
#     def patch(self):
#         pass
#     def delete(self):
#         pass
# api.add_resource(Transactions, '/transactions')


# class TransactionsById(Resource):
#     def get(self):
#         pass
#     def post(self):
#         pass
#     def patch(self):
#         pass
#     def delete(self):
#         pass
# api.add_resource(TransactionsById, '/transactions/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
