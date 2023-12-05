[![gate](https://github.com/chungg/fullstack-flask/actions/workflows/gate.yml/badge.svg)](https://github.com/chungg/fullstack-flask/actions/workflows/gate.yml)

# flask + htmx + bulma

sample app which provides:
- backend
  - backend via [apiflask](https://github.com/apiflask/apiflask)
  - db via [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
  - config management via [dotenv](https://github.com/theskumar/python-dotenv)
  - security via [flask-security-too](https://github.com/Flask-Middleware/flask-security)
  - admin views via [flask-admin](https://github.com/flask-admin/flask-admin)
  - package management via [pipenv](https://github.com/pypa/pipenv)
  - cli via [click](https://github.com/pallets/click) and [rich](https://github.com/Textualize/rich)
- ui
  - frontend via [htmx](https://github.com/bigskysoftware/htmx) and [jinja](https://github.com/pallets/jinja)
  - styling via [bulma](https://github.com/jgthms/bulma)
  - charting via [chartjs](https://www.chartjs.org/)
  - tables via [tabulator](https://tabulator.info/)
- test
  - runner via [pytest](https://github.com/pytest-dev/pytest)
  - system testing via [playwright](https://github.com/microsoft/playwright)
  - ci via [gitub actions](https://github.com/features/actions)

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

### permissions

#### init

- ENV=local pipenv run flask --app app.app roles create superuser
- ENV=local pipenv run flask --app app.app users create <email> -a

#### details

- ENV=local pipenv run flask --app app.app show roles

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

- SQLALCHEMY_DATABASE_URI=<postgres_uri> pipenv run pytest tests/unit
- see github actions workflow for sample

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
- chart options - https://www.monterail.com/blog/javascript-libraries-data-visualization
- alt reactive tables
  - [grid.js](https://gridjs.io/) - seems to mildly inactive, simpler functionality
  - [tanstack](https://tanstack.com/table) - docs are not helpful if not using framework
  - [glide](https://grid.glideapps.com/) - requires react
  - [ag-grid](https://www.ag-grid.com/) - requires money
- htmx
  - https://blog.ohheybrian.com/2023/06/smarter-templating-with-htmx-and-flask/
  - https://www.advantch.com/blog/how-to-build-interactive-charts-in-python-using-htmx-and-echarts/
  - https://github.com/Konfuzian/htmx-examples-with-flask

# todo
- more frontend via htmx https://htmx.org/docs/
- customise bulma via https://bulma.io/documentation/customize/
- worker processes? via ?
- optimised ci via [mergify](https://mergify.com/)
- https://unsuckjs.com/
