# Ticketing-System

Ticketing management system made with Django and directly works with telegram bots using [Telethon](https://docs.telethon.dev/en/stable/).

To set up the project, follow the steps below:

 1. run `pip install -r requirements.txt` to install all necessary libraries in python
 2. run `python manage.py collectstatic` in order for **django** and
    **summernote** to import all its files into static folder in the root
    directory.
 3. fill out settings.py file in `System` folder: database and telegram bot credentials. You also should add your domain name in `ALLOWED_HOSTS`

As [Telethon](https://docs.telethon.dev/en/stable/) is an asyncronous library, you have to run two commands in seperate terminals: 
 1. `python manage.py runserver` for django project
 2. `python manage.py run_bot` for telegram bot
