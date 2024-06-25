# Backend API

REST APIs for Odoo assignment app.

## Project Setup

```sh
cd api
python3.11 -m venv env
```

### Activate the virtual env
```sh
source env/bin/activate
```

### Install dependencies
```sh
pip install -r requirements.txt
```

### Apply the migrations

```sh
cd api
source env/bin/activate
python manage.py migrate
```

### Run django application Server
```sh
python manage.py runserver
```

### Create superuser
```sh
python manage.py createsuperuser
```

### Create login user
- Go to the django admin panel after creating superuser.
- Add a normal user by going to user management section.

## Docs

- This project contains four api which are documented as postman collection which can be found in `./docs` folder.

## Generate Credentials
```sh
curl --location 'http://127.0.0.1:8000/api/auth/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "user1",
    "password": "user1@1234"
}'
```