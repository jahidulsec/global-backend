#!/bin/bash

# Build the project
echo "Building the project..."
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install django-phonenumbers


echo "Collect Static..."
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic