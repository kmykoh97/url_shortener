#!/bin/bash
python urlshortener/manage.py makemigrations
python urlshortener/manage.py makemigrations tinyurl
python urlshortener/manage.py migrate
python urlshortener/manage.py runserver 0.0.0.0:8001
