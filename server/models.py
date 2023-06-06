# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique = True, nullable = False)
    _password_hash = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)

    cart_items = db.relationship("Cart_Item", backref= "user")

    serialize_rules = ('-cart_items.user',)

    def __repr__(self):
        return f'<User {self.id}: {self.name}>'

    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    units = db.Column(db.Integer)
    units_sold = db.Column(db.Integer)
    image_url = db.Column(db.String)

    cart_items = db.relationship("Cart_Item", backref= "product")

    serialize_rules = ('-cart_items.product',)

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'
    
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    purchased = db.Column(db.Boolean, default=False)

    cart_items = db.relationship("Cart_Item", backref= "order")

    serialize_rules = ('-cart_items.order',)

    def __repr__(self):
        return f'<Order {self.id}>'
    
class Cart_Item(db.Model, SerializerMixin):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    serialize_rules = ('-user.cart_items', '-product.cart_items', '-order.cart_items')

    def __repr__(self):
        return f'<Cart Item {self.id}>'


# Models go here!
