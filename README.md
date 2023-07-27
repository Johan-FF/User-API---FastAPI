# User-API---FastAPI

This is a Python project built with FastAPI that provides basic CRUD operations (Create, Read, Update, Delete) for managing users, along with authentication using JWT tokens.

## Requirements

- Python 3.10+
- FastAPI
- SQLAlchemy
- PyJWT

## Installation

1. Clone the repository:

~~~
git clone https://github.com/Johan-FF/User-API---FastAPI.git
cd User-API---FastAPI
~~~

2. Create a virtual environment (optional but recommended):

~~~
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
~~~

3. Install the dependencies:

~~~
pip install -r requirements.txt
~~~

## Configuration

Before running the application, make sure to configure the database connection in User-API--FastAPI/config/database.py and configure the CORS in User-API--FastAPI/main.py:

~~~
origins = [
    "http://localhost",
    "http://localhost:4200",
]
~~~

Now, create a User-API--FastAPI/conf.py file with a secret key: 

~~~
SECRET_KEY = "Put your secret key here"
~~~

## Usage

Run the FastAPI application with:

~~~
uvicorn app.main:app --reload
~~~

This will start the development server, and you can access the API documentation (Swagger) at http://localhost:8000/docs.

To authenticate, make a POST request to /users/login with valid user credentials (username and password). This will provide you with a JWT token.

Include the obtained JWT token in the Authorization header for all subsequent requests to access protected routes.

This project can work in conjunction with the repository: [https://github.com/Johan-FF/Paint-Project---Angular-js.git](https://github.com/Johan-FF/Paint-Project---Angular-js.git)
This will allow logging in and drawing in the user interface of the other repository.
