# Ticketing-System

  
Ticketing management system made with Django and directly works with telegram bots using [Telethon](https://docs.telethon.dev/en/stable/).


To set up the project, follow the steps below:

  1. Installing python version below 3.12 is recommended as there have been some issues with Python 3.12
  2. Create a virtual environment using commands `python -m venv <venv name>`
  3. Activate your virtual environment with `source /path/to/venv`
  4. Clone the repository and run `pip install -r requirements.txt` to install all necessary libraries
  5. Run `python manage.py collectstatic` in order for **django** and **summernote** to import all its files into static folder in the root directory of project
  6. Fill out settings.py file in `System` folder: database and telegram bot credentials. You also should add your domain name in `ALLOWED_HOSTS`

  
As [Telethon](https://docs.telethon.dev/en/stable/) is an asyncronous library, you have to run two commands in seperate terminals:

1.  `python manage.py runserver` for django project
2.  `python manage.py run_bot` for telegram bot