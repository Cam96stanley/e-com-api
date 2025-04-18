from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Table, Column, ForeignKey, select
from datetime import datetime, timezone
from typing import List

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Cam.110196@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

# ========== Association Table ==========

order_product = Table(
  "order_product",
  Base.metadata,
  Column("order_id", ForeignKey("orders.id"), primary_key=True),
  Column("product_id", ForeignKey("products.id"), primary_key=True)
)

# ========== Models ==========

class User(Base):
  __tablename__ = "users"
  
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(30), nullable=False)
  address: Mapped[str] = mapped_column(String(100), nullable=False)
  email: Mapped[str] = mapped_column(String(50), unique=True)
  
  orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")
  

class Order(Base):
  __tablename__ = "orders"
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  order_date: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc))
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
  
  user: Mapped["User"] = relationship("User", back_populates="orders")
  products: Mapped[List["Product"]] = relationship("Product", secondary=order_product, back_populates="orders")
  

class Product(Base):
  __tablename__ = "products"
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  product_name: Mapped[str] = mapped_column(String(50), nullable=False)
  price: Mapped[float] = mapped_column(nullable=False)
  
  orders: Mapped[List["Order"]] = relationship("Order", secondary=order_product, back_populates="products")
  

# ========== Schemas ==========

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User

class OrderSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Order
    include_fk = True
    
class ProductSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Product
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# ========== User Routes ==========

# Get All Users
@app.route('/users', methods=['GET'])
def get_users():
  query = select(User)
  users = db.session.execute(query).scalars().all()
  if not users:
    return jsonify({"message": "No users found"}), 404
  return users_schema.jsonify(users), 200

# Get One User
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
  user = db.session.get(User, user_id)
  if not user:
    return jsonify({"message": "User not found"}), 404
  return user_schema.jsonify(user), 200

# Create User
@app.route('/users', methods=['POST'])
def create_user():
  try:
    user_data = user_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400
  new_user = User(name=user_data['name'], address=user_data['address'], email=user_data['email'])
  db.session.add(new_user)
  db.session.commit()
  return user_schema.jsonify(new_user), 201

# Update User
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
  user = db.session.get(User, user_id)
  if not user:
    return jsonify({"message": "User not found"}), 404
  try:
    user_data = user_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400
  user.name = user_data['name']
  user.address = user_data['address']
  user.email = user_data['email']
  db.session.commit()
  return user_schema.jsonify(user), 200

# Delete User
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  user = db.session.get(User, user_id)
  if not user:
    return jsonify({"message": "Invalid user id"})
  db.session.delete(user)
  db.session.commit()
  return jsonify({"message": f"Succesfully deleted user {user_id}"})

# ========== Product Routes ==========

# Get All Products
@app.route('/products', methods=['GET'])
def get_products():
  query = select(Product)
  products = db.session.execute(query).scalars().all()
  if not products:
    return jsonify({"message": "No products found"}), 404
  return products_schema.jsonify(products), 200

# Get One Product
@app.route('/products/<int:prod_id>', methods=['GET'])
def get_product(prod_id):
  product = db.session.get(Product, prod_id)
  if not product:
    return jsonify({"message": "Invalid product id"})
  return product_schema.jsonify(product)

# Create Product
@app.route('/products', methods=['POST'])
def create_product():
  try:
    product_data = product_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400
  new_product = Product(product_name=product_data['product_name'], price=product_data['price'])
  db.session.add(new_product)
  db.session.commit()
  return product_schema.jsonify(new_product), 201
    
# Update Product
@app.route('/products/<int:prod_id>', methods=['PUT'])
def update_product(prod_id):
  product = db.session.get(Product, prod_id)
  if not product:
    return jsonify({"message": "Product not found"}), 404
  try:
    product_data = product_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400
  product.product_name = product_data['product_name']
  product.price = product_data['price']
  db.session.commit()
  return product_schema.jsonify(product), 200

# Delete Product
@app.route('/products/<int:prod_id>', methods=['DELETE'])
def delete_product(prod_id):
  product = db.session.get(Product, prod_id)
  if not product:
    return jsonify({"message": "Product not found"}), 404
  db.session.delete(product)
  db.session.commit()
  return jsonify({"message": f"Succesfully deleted product {prod_id}"}), 200


# ========== Order Routes ===========

# Get All Orders for User
@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders(user_id):
  user = db.session.get(User, user_id)
  if not user:
    return jsonify({"message": "User not found"}), 404
  return orders_schema.jsonify(user.orders), 200

# Get All Products for Order
@app.route('/orders/<int:order_id>/products', methods=['GET'])
def get_order_prods(order_id):
  order = db.session.get(Order, order_id)
  if not order:
    return jsonify({"message": "Order not found"}), 404
  return products_schema.jsonify(order.products), 200

# Create Order
@app.route('/orders', methods=['POST'])
def create_order():
  try:
    order_data = order_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400
  new_order = Order(user_id=order_data['user_id'])
  db.session.add(new_order)
  db.session.commit()
  return order_schema.jsonify(new_order)

# Add Product to Order
@app.route('/orders/<int:order_id>/add_product/<int:prod_id>', methods=['PUT'])
def add_product_order(order_id, prod_id):
  order = db.session.get(Order, order_id)
  product = db.session.get(Product, prod_id)
  if not order or not product:
    return jsonify({"message": "Order or Product not found"}), 404
  if product in order.products:
    return jsonify({"message": f"{product.product_name} is already in order number {order.id}"}), 400
  order.products.append(product)
  db.session.commit()
  return jsonify({"message": f"{product.product_name} has been added to order number {order.id}"})
  
# Delete Product from Order
@app.route('/orders/<int:order_id>/remove_product', methods=['DELETE'])
def delete_order_product(order_id):
  order = db.session.get(Order, order_id)
  if not order:
    return jsonify({"message": "No order found"}), 404
  product_id = request.json.get('product_id')
  if not product_id:
    return jsonify({"message": "Missing product_id in request body"}), 400
  product = db.session.get(Product, product_id)
  if not product:
    return jsonify({"message": "No product found"}), 404
  if product not in order.products:
    return jsonify({"message": "Product not associated with this order"}), 400
  order.products.remove(product)
  db.session.commit()
  return jsonify({"message": f"{product.product_name} removed from order number {order.id}"}), 200

# ========== Start Server ==========

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)