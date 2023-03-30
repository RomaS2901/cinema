# cinema

Create virtual environment:
`virtualenv venv -p python3.11`

Activate virtual environment:
`source venv/bin/activate`

Install requirements:
`pip install -r requirements.txt`

Create superuser:
`python manage.py createsuperuser`

Migrate db schema:
`python manage.py migrate`

Run development server
`python manage.py runserver 8000`

Swagger docs to API can be found here:

`http://127.0.0.1:8000/api/schema/swagger-ui/`

`http://127.0.0.1:8000/api/schema/redoc/`

Run tests:
`python -m pytest tests/`