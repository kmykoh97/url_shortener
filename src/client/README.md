# Url Shortener client

Here, we implement our service client using django(frontend+backend)

## Advantage

- Django is easily scalable for multinodes.
- Django can provide frontend and backend for us.
- Django allows us to use Python libraries freely.
- Unit test in Django is a lot easier than framework like Spring.

## How to use

For ease of development, everything is written in Dockerfiles and is able to fire up using one liner. 

However if one wishes to do local debugging, run:
```sh
python -m venv venv # for virtual environment
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py test # optional, for testing
python manage.py runserver
```
Remember to set DB to sqlite3 in `urlshortener/settings.py` for local development because we are not using any container

