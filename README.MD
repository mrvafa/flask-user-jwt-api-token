# Blog API

This is sample JWS API for flask framework.

## Table of content

1. [Installation](#installation)
2. [Usage examples](#usage-examples)
3. [TODO](#todo)

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


  |METHOD|             url                 | required fields|description|
  |------|---------------------------------|----------------|---| 
  | POST | http://127.0.0.1:5000/register  | username, email, password| Create user| 
  | POST | http://127.0.0.1:5000/login     | username, password| Login via username and password|
  | POST | http://127.0.0.1:5000/login     | email, password| Login via email and password|
  | GET  | http://127.0.0.1:5000/profile/<user-id> | None | Get user info |
  | PUT  | http://127.0.0.1:5000/profile/ | username or email | Edit my profile (auth token required) |

<a name="todo"></a>

## TODO

- [X] Start and set flask.
- [X] Create user model.
- [X] Create user views and urls.
- [X] Add test.
- [X] Add password, email and username validator.
- [ ] Add fields like birthday, last_login, image profile and phone_number.