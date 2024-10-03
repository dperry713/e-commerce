# E-Commerce API

This is a Flask-based RESTful API for an e-commerce application. It provides endpoints for managing customers, customer accounts, products, and orders.

## Features

- Customer management (CRUD operations)
- Customer account management with secure password hashing
- Product management (CRUD operations)
- Order placement and management
- Stock tracking for products
- Order cancellation with stock adjustment
- Order total calculation

## Setup

1. Install the required dependencies:
   ```bash
   pip install flask flask_sqlalchemy werkzeug
Set up your MySQL database and update the SQLALCHEMY_DATABASE_URI in app.py with your database credentials.

python app.py

API Endpoints
Customers
POST /customers - Create a new customer
GET /customers/<customer_id> - Retrieve a customer
PUT /customers/<customer_id> - Update a customer
DELETE /customers/<customer_id> - Delete a customer
Customer Accounts
POST /customer-accounts - Create a new customer account
GET /customer-accounts/<account_id> - Retrieve a customer account
PUT /customer-accounts/<account_id> - Update a customer account
DELETE /customer-accounts/<account_id> - Delete a customer account
Products
POST /products - Create a new product
GET /products/<product_id> - Retrieve a product
PUT /products/<product_id> - Update a product
DELETE /products/<product_id> - Delete a product
GET /products - List all products
Orders
POST /orders - Place a new order
GET /orders/<order_id> - Retrieve an order
POST /orders/<order_id>/cancel - Cancel an order
GET /orders/<order_id>/total - Calculate the total price of an order
Models
The application uses the following database models:

Customer
CustomerAccount
Product
Order
OrderItem
Security
Passwords are securely hashed using Werkzeug's security functions.
Input validation is performed to ensure data integrity.
Error Handling
The API uses appropriate HTTP status codes and returns JSON responses for both successful operations and errors.

Development
This application runs in debug mode by default. For production deployment, make sure to turn off debug mode and use a production-ready WSGI server.

