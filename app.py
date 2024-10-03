from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:irrelevant1@127.0.0.1:3306/customer_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    accounts = db.relationship('CustomerAccount', backref='customer', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)

class CustomerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Customer endpoints
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully', 'id': new_customer.id}), 201

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone
    })

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.json
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

# CustomerAccount endpoints
@app.route('/customer-accounts', methods=['POST'])
def create_customer_account():
    data = request.json
    customer = Customer.query.get_or_404(data['customer_id'])
    new_account = CustomerAccount(username=data['username'], customer_id=customer.id)
    new_account.set_password(data['password'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'message': 'Customer account created successfully', 'id': new_account.id}), 201

@app.route('/customer-accounts/<int:account_id>', methods=['GET'])
def get_customer_account(account_id):
    account = CustomerAccount.query.get_or_404(account_id)
    return jsonify({
        'id': account.id,
        'username': account.username,
        'customer_id': account.customer_id
    })

@app.route('/customer-accounts/<int:account_id>', methods=['PUT'])
def update_customer_account(account_id):
    account = CustomerAccount.query.get_or_404(account_id)
    data = request.json
    account.username = data.get('username', account.username)
    if 'password' in data:
        account.set_password(data['password'])
    db.session.commit()
    return jsonify({'message': 'Customer account updated successfully'})

@app.route('/customer-accounts/<int:account_id>', methods=['DELETE'])
def delete_customer_account(account_id):
    account = CustomerAccount.query.get_or_404(account_id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Customer account deleted successfully'})

# Product endpoints
@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'], stock=data.get('stock', 0))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully', 'id': new_product.id}), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'stock': product.stock
    })

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'stock': product.stock
    } for product in products])

# Order endpoints
@app.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    new_order = Order(customer_id=data['customer_id'])
    for item in data['items']:
        product = Product.query.get_or_404(item['product_id'])
        if product.stock < item['quantity']:
            return jsonify({'message': f'Insufficient stock for product {product.name}'}), 400
        order_item = OrderItem(product_id=item['product_id'], quantity=item['quantity'])
        new_order.items.append(order_item)
        product.stock -= item['quantity']
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully', 'id': new_order.id}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'customer_id': order.customer_id,
        'order_date': order.order_date,
        'status': order.status,
        'items': [{
            'product_id': item.product_id,
            'quantity': item.quantity
        } for item in order.items]
    })

@app.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != 'Pending':
        return jsonify({'message': 'Cannot cancel order that is not pending'}), 400
    order.status = 'Cancelled'
    for item in order.items:
        item.product.stock += item.quantity
    db.session.commit()
    return jsonify({'message': 'Order cancelled successfully'})

@app.route('/orders/<int:order_id>/total', methods=['GET'])
def calculate_order_total(order_id):
    order = Order.query.get_or_404(order_id)
    total = sum(item.product.price * item.quantity for item in order.items)
    return jsonify({'order_id': order.id, 'total_price': total})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
