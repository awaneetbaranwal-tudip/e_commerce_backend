# E-commerce Backend System Development (e_commerce_1)

Develop a backend system for an e-commerce platform using Python and Django. The system should support product management, user orders, and an analytics dashboard. 

## Programming Language and Framework
- Python
- Django Rest Framework

## List of Apps in the Project
- `users`,
- `users_cart`
- `order_items`,
- `orders`,
- `products`,

## Services
- Google OAuth 2.0

## Databases
- MySQL

## List of APIs

- **Get All Products**: Fetches all products available in the store.
  - Endpoint: `/products/`
  - Method: GET

- **Get Product by ID**: Fetches details of a specific product by its ID.
  - Endpoint: `/products/<int:pk>/`
  - Method: GET

- **Add Product**: Allows adding a new product to the store.
  - Endpoint: `/products/`
  - Method: POST

- **Update Product**: Allows updating an existing product in the store.
  - Endpoint: `/product/update/<int:pk>/`
  - Method: PUT

- **Delete Product**: Deletes a product from the store based on its ID.
  - Endpoint: `/product/<int:pk>/`
  - Method: DELETE

- **Add Category**: Adds a new category for products.
  - Endpoint: `/category/`
  - Method: POST

- **Update Category**: Update category for products.
  - Endpoint: `/category/update/<int:pk>`
  - Method: POST

- **Get All Category**: Fetches all categories for products.
  - Endpoint: `/categories/`
  - Method: POST

- **Delete Category**: Deletes a category based on its ID.
  - Endpoint: `/category/<int:pk>`
  - Method: POST

- **Add Product to Cart**: Adds a product to the user's shopping cart.
  - Endpoint: `/cart/`
  - Method: POST

- **Update Cart Product**: Updates the quantity of a product in the user's shopping cart.
  - Endpoint: `cart/update/<int:pk>/`
  - Method: PUT

- **Get All Cart Products**: Fetches all products in the user's shopping cart.
  - Endpoint: `/cart/products/`
  - Method: GET

- **Delete Cart Product**: Removes a product from the user's shopping cart.
  - Endpoint: `/cart/<int:pk>/`
  - Method: DELETE

- **Place Order**: Allows users to place an order for the items in their shopping cart.
  - Endpoint: `/order/`
  - Method: POST

- **List Users**: Fetches a list of all users registered in the system.
  - Endpoint: `/users/`
  - Method: GET

- **User Authentication**: 
  - **Login**: Users can manually log in using their email ID and password.
    - Endpoint: `/login/`
    - Method: POST
  - **Register**: Users can create a new account.
    - Endpoint: `/register/`
    - Method: POST
  - **User Details**: Fetches details of the authenticated user.
    - Endpoint: `/user/`
    - Method: GET
  - **Logout**: Logs out the authenticated user.
    - Endpoint: `/logout/`
    - Method: GET

- **Address Management**: 
  - **List Addresses**: Fetches a list of all addresses associated with the authenticated user.
    - Endpoint: `/addresses/`
    - Method: GET
  - **Address Detail**: Fetches details of a specific address by its ID.
    - Endpoint: `/addresses/<int:pk>/`
    - Method: GET
- **Allauth Accounts**: Integrates Django Allauth for user authentication and account management, including features like sign-up, login, password reset, etc.
  - Endpoint: `/accounts/`
  - Method: GET, POST, PUT, DELETE

This endpoint includes various sub-endpoints provided by Django Allauth for user account management, such as:

  - **Signup**: Allows users to register/sign up for a new account using email and password.
    - Endpoint: `/accounts/signup/`
    - Method: POST

  - **Login**: Enables users to log in to their existing accounts using their credentials.
    - Endpoint: `/accounts/login/`
    - Method: POST

  - **Logout**: Logs out the currently authenticated user.
    - Endpoint: `/accounts/logout/`
    - Method: POST

  - **Password Reset**: Allows users to request a password reset if they have forgotten their password.
    - Endpoint: `/accounts/password/reset/`
    - Method: POST

  - **Password Change**: Allows users to change their passwords after logging in.
    - Endpoint: `/accounts/password/change/`
    - Method: POST

  - **Email Confirmation**: Handles email confirmation for user accounts.
    - Endpoint: `/accounts/confirm-email/`
    - Method: GET

  - **Email Verification Sent**: Notifies users that an email verification link has been sent to their email.
    - Endpoint: `/accounts/email/`
    - Method: GET

  - **Email Change**: Allows users to change the email associated with their account.
    - Endpoint: `/accounts/email/change/`
    - Method: POST

  - **Social Account Connections**: Integrates social account connections, such as Google OAuth 2, for sign-up and login.
    - Endpoint: `/accounts/social/connections/`
    - Method: GET, POST, PUT, DELETE

  - **Profile Edit**: Allows users to edit their profile information.
    - Endpoint: `/accounts/profile/`
    - Method: GET, PUT, DELETE

## Dependencies

- `Django`
- `sqlparse`
- `django-filter`
- `djangorestframework`
- `django-cors-headers`
- `PyMySQL`
- `requests`
- `django-countries`
- `PyJWT`
- `requests`


## Running the Project Locally

To run the e_commerce_1 project locally, follow these steps:

### Prerequisites

- Install Python (3.7 or higher): [Python Installation Guide](https://www.python.org/downloads/)

### Setting up the Environment

1. Clone this repository to your local machine:

   ```
   git clone https://github.com/folder-name/e_commerce_1.git
   ```

2. Navigate to the project directory:

   ```
   cd e_commerce_1
   ```

3. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```
     source venv/bin/activate
     ```

### Installing Dependencies

1. Install required Python packages using pip:

   ```
   pip install -r requirements.txt
   ```

### Database Configuration

1. Configure the database settings in the `e_commerce_1/settings.py` file. You'll need to set up your MySQL and MongoDB connection details.

### Running Migrations

1. Run the database migrations to create the necessary database schema:
    ```
   python manage.py makemigrations
   ```

   ```
   python manage.py migrate
   ```

### Running the Development Server

1. Start the Django development server:

   ```
   python manage.py runserver
   ```

2. Your e_commerce_1 should now be running locally at `http://127.0.0.1:8000/`.


### e_commerce_1 Documentations:
- [e_commerce_1 Doc](https://docs.google.com/document/d/1VHSJwNt4qgbcWueKbe1ml-0q12aHfIoBGjoGlTxEnzQ/edit)
- [List of e_commerce_1 URLs]()