# 🛒 E-Com-API

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey?logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=sqlite)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?logo=mysql)

---

## 📌 About the Project

**E-Com-API** is a RESTful API built during my time at [Coding Temple](https://www.codingtemple.com/). It serves as the backend for a basic e-commerce system, using Flask and SQLAlchemy ORM to interact with a MySQL database.

The project includes:

- Three core models: `User`, `Product`, and `Order`
- An association table for the many-to-many relationship between Orders and Products
- Marshmallow schemas for serialization and validation
- Multiple API endpoints for full CRUD functionality

## 🏗️ Technologies Used

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Marshmallow](https://marshmallow.readthedocs.io/)
- [MySQL](https://www.mysql.com/)
- [Postman](https://www.postman.com/) for API testing

## 📁 Project Structure

```bash
e-com-api/
├── app.py # Main Flask application with models and api calls
├── requirements.txt # Python dependencies
├── .gitignore # Files to exclude from version control
```

## 🚀 Setup Instructions

Follow these steps to set up and run the E-Com API locally:

### 1. Clone the Repository

```bash
git clone https://github.com/Cam96stanley/e-com-api.git
cd e-com-api
```

### 2. Create and Activate a Virtual Environment

For Linux/MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Your Database

Make sure you have a MySQL server running and create a database named **_ecommerce_api_**
Update your database URI in **_app.py_**:

```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/ecommerce_api'
```

### 5. Run the Application

```bash
python app.py
```

The API should now be running at ***http://127.0.0.1:5000/***.

## 🔌 API Endpoints

#### Users

| Method | Route                  | Description       |
| ------ | ---------------------- | ----------------- |
| GET    | `/users`               | Get all users     |
| GET    | `/users/<int:user_id>` | Get a single user |
| POST   | `/users`               | Add a new user    |
| PUT    | `/users/<int:user_id>` | Update user       |
| DELETE | `/users/<int:user_id>` | Delete a user     |

#### Products

| Method | Route                     | Description          |
| ------ | ------------------------- | -------------------- |
| GET    | `/products`               | Get all products     |
| GET    | `/products/<int:prod_id>` | Get a single product |
| POST   | `/products`               | Create a new product |
| PUT    | `/products/<int:prod_id>` | Update product       |
| DELETE | `/products/<int:prod_id>` | Delete product       |

#### Orders

| Method | Route                                              | Description                    |
| ------ | -------------------------------------------------- | ------------------------------ |
| GET    | `/orders/user/<int:user_id>`                       | Get all orders for a user      |
| GET    | `/orders/<int:order_id>/products`                  | Get all products for an order  |
| POST   | `/orders`                                          | Create a new order             |
| PUT    | `/orders/<int:order_id>/add_product/<int:prod_id>` | Update product                 |
| DELETE | `/orders/<int:prod_id>/remove_product`             | Delete a product from an order |

## 🧰 Features

- **User Management**:

  - Create new users with their information (name, address, email).
  - View a list of all users in the database.

- **Product Management**:

  - Add new products to the catalog with a name and price.
  - Retrieve a list of all available products.

- **Order Management**:

  - Create new orders for users.
  - Add products to an order.
  - Remove products from an order.
  - View all products associated with a specific order.

- **Association of Orders and Products**:
  - Use an association table to link products to orders, allowing flexibility in managing order contents.

## 🧪 Testing

Use [Postman](https://www.postman.com) to test endpoints. You can test all routes using JSON requests and instpect reponses directly.

## 🛠 Future Enhancements

The following features and improvements are planned for future versions of the E-Com-API:

1. **Authentication & Authorization**:

   - Implement user authentication using JWT to secure API endpoints and allow users to register, login, and access protected resources.

2. **Order History**:

   - Add an endpoint to view a user's order history, showing all previous orders and associated products.

3. **Product Categories**:

   - Implement product categories (e.g., electronics, clothing) to better organize the products and allow filtering by category.

4. **Shopping Cart**:

   - Introduce a shopping cart feature where users can add products to their cart before completing the order.

5. **Improved Error Handling**:

   - Implement more detailed error messages and status codes to improve the user experience when interacting with the API.

6. **Admin Dashboard**:

   - Develop an admin dashboard for managing users, products, and orders from a web interface.

7. **Product Reviews**:
   - Allow users to leave reviews and ratings for products, enhancing user engagement.

These enhancements will be incorporated in future releases to improve functionality and usability.

## 📧 Contact

Cameron Stanley - [LinkedIn](https://www.linkedin.com/in/cameron-stanley-007908339/) - cam96stanley@gmail.com

Project Link: [https://github.com/Cam96stanley/e-com-api](https://github.com/Cam96stanley/e-com-api)
