# Flask User JWT API Token

This is sample JWS API for flask framework.

## Table of content

1. [Installation](#installation)
2. [Usage examples](#usage-examples)
3. [File Structure](#file-structure)
4. [Tests](#tests)
5. [TODO](#todo)

<a name="installation"></a>

## Installation

- Clone the repository.
- Make sure `Python 3.8` is installed.
- Create virtual environment using `python -m virtualenv --python=python3 env`.
- Activate env (in linux use `. env/bin/activate`).
- Install requirements.txt using `pip install -r requirements.txt`.
- Create .env file (`cp .env.template .env`).
- Fill the `.env` file.
    - set `SECRET_KEY` to some strong random key (e.g `os.urandom(12).hex()`).

<a name="usage-examples"></a>

## Usage examples

1. Setup flask database.

`./manage.py create_db`

2. Run the server

`./manage.py runserver`

3. Create user

|METHOD|             url                 | required fields|headers|description|
  |------|---------------------------------|----------------| --- |---| 
| POST | http://127.0.0.1:5000/register  | username, email, password| None|Create user| 
| POST | http://127.0.0.1:5000/login     | username, password| None |Login via username and password|
| POST | http://127.0.0.1:5000/login     | email, password| None| Login via email and password|
| GET  | http://127.0.0.1:5000/profile/<user-id> | None | None| Get user info |
| PUT  | http://127.0.0.1:5000/profile/ | username or email | token|Edit my profile (auth token required) |

<a name="file-sturcture"></a>

## File Structure

```
Task1
└── project                   # project packge
    ├── __init__.py           # Config flask app 
    ├── Validators.py         # Validator for email, username and password
    ├── User
    │    ├── __init__.py
    │    ├── tests.py         # unittest for user model
    │    ├── models.py        # User model
    │    └── api
    │        ├── __init__.py  
    │        ├── tests.py     # API test for API user
    │        ├── urls.py      # API urls for API user
    │        └── views.py     # API Views
    │
    ├── README.ME             # file to help setup
    ├── LICENCE               # licenece file (MIT)
    ├── db.sqlite3            # Project database
    ├── db.sqlite3_test       # Test database
    ├── .env                  # Private varables 
    ├── .env.template         # Template for .env
    ├── requirements.txt      # Packages that are required
    ├── manage.py             # File to manage flask
    ├── config.py             # Default config 
    └── env                   # Python enviroment
```

- [X] Start and set flask.
- [X] Create user model.
- [X] Create user views and urls.
- [X] Add test.
- [X] Add password, email and username validator.
- [ ] Add fields like birthday, last_login, image profile and phone_number.

<a name="tests"></a>

## Tests

> To run flask tests run `./manage.py test`

<a name="todo"></a>

## TODO

- [X] Start and set flask.
- [X] Create user model.
- [X] Create user views and urls.
- [X] Add test.
- [X] Add password, email and username validator.
- [ ] Add fields like birthday, last_login, image profile and phone_number.
