# flask + htmx + bulma

sample app which provides:
- backend via [apiflask](https://github.com/apiflask/apiflask)
- db via [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
- config management via [dotenv](https://github.com/theskumar/python-dotenv)
- frontend via [htmx](https://github.com/bigskysoftware/htmx) and [jinja](https://github.com/pallets/jinja) (because i was too lazy to override security endpoints)
- styling via [bulma](https://github.com/jgthms/bulma)
- security via [flask-security-too](https://github.com/Flask-Middleware/flask-security)
- testing via [pytest](https://github.com/pytest-dev/pytest)
- system testing via [playwright](https://github.com/microsoft/playwright)
- admin views via [flask-admin](https://github.com/flask-admin/flask-admin)
- package management via [pipenv](https://github.com/pypa/pipenv)
- cli via [click](https://github.com/pallets/click) and [rich](https://github.com/Textualize/rich)

## setup

- install system requirements
  - debian/ubuntu - `sudo apt install libpq-dev postgresql pipenv`
- install python reqs - `pipenv install`
- configure db
  - `sudo -u postgres psql`
  - `create database <dbname>;`
  - `create user <user> with encrypted password '<pw>';`
  - `grant all privileges on database <dbname> to <user>;`
  - `create schema <schema>;`
  - `grant all on schema <schema> to <user>;`

## configuring

config options can be found at app/config.py. at a minimum, the following options need to be set:
- SQLALCHEMY_DATABASE_URI
- SECRET_KEY (run `secrets.token_urlsafe()` if not sure)
- SECURITY_PASSWORD_SALT (run `secrets.SystemRandom().getrandbits(128)` if not sure)

you will need to create and assign a `superuser` role to the user to see model views in Admin

### auth providers

todo how to set up external providers

## managing

### migrations

#### autogen migrations

- ENV=local pipenv run flask --app app.app db migrate -m '<description>' --directory app/storage/migrations

#### apply

- ENV=local pipenv run flask --app app.app db upgrade --directory app/storage/migrations

#### init (if starting from scratch or you want to compress migrations)

- ENV=local pipenv run flask --app app.app db init --directory app/storage/migrations

## running

### server

- ENV=local pipenv run flask --app app.app run --debug

### client

    import requests
    sess = requests.Session()
    sess.post('http://127.0.0.1:5000/api/login',
              data={'email':'<email>','password':'<pw>', 'remember': 'false'},
              headers={"Content-Type": "application/x-www-form-urlencoded"})
    # session should have cookie
    sess.cookies

## running tests

- pipenv install --dev

### styling

- pipenv run flake8

### unit

- pipenv run pytest tests/unit

### system

#### setup

- pipenv run playwright install

#### run

- ENV=local pipenv run flask --app app.app run
- TEST_USER=<user> TEST_PW=<pw> pipenv run pytest tests/system

#### debug

- TEST_USER=<user> TEST_PW=<pw> pipenv run pytest tests/system -k <test_case> --headed --slowmo 1000

## resources

- flask-security:
  - https://github.com/mattupstate/flask-security/issues/769
  - oauth configuration:
    - https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask-in-2023
    - https://flask-security-too.readthedocs.io/en/stable/features.html#social-oauth-authentication
- flask deep dives (tbh, i didn't read/watch these but so i clear bookmarks):
  - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
  - https://hackersandslackers.com/flask-user-sessions-and-redis/
  - https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
- bulma
  - templates - https://github.com/BulmaTemplates/bulma-templates
  - buttons - https://github.com/aldi/bulma-social

# todo
- more frontend via htmx https://htmx.org/docs/
- customise bulma via https://bulma.io/documentation/customize/
- charts via https://echarts.apache.org/en/index.html
- tables via https://datatables.net/
- worker processes? via ?
