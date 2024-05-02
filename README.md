![Static Badge](https://img.shields.io/badge/License-MIT-green) ![Static Badge](https://img.shields.io/badge/django-v5.0.x-blue?logo=django) ![Static Badge](https://img.shields.io/badge/Telethon-v1.33.1-blue?logo=telegram&logoColor=blue)


# Ticketing-System written in Django
Ticketing management system made with Django and directly works with telegram bots using [Telethon](https://docs.telethon.dev/en/stable/)

### Features
- Receiving queries through telegram 
- Managing many tickets at the same time
- Supports multilanguages
- Informs moderators of exception and errors

### Requirements
Django version for the project is 5.0 and supports Python 3.10 and later. But there were some problems with Python 3.12, so it is recommended to use [Python 3.10 - 3.11](https://www.python.org/downloads/)

### Installation
 1. Assuming you have Python installed in your machine, you have to create a virtual environment to deploy the project.
 ```bash
python -m venv /path/to/new/virtual/environment
```
 2. Activate your virtual environment
**For Windows:**
```bash
/venv-folder/scripts/activate
````
**For Linux:**
```bash
source /venv-folder/bin/activate
```
3. Clone the repository and run the command below to install all necessary libraries
```bash
pip install -r requirements.txt 
```

### Configuring setting.py file
`System/settings.py` file contains all the configuration of your Django project and is just a Python module with module-level variables.

```python
27  DEBUG=False
28  ALLOWED_HOSTS = ["your.domain.com"]
```
You should enter the production domain name in `ALLOWED_HOSTS`, otherwise you will get an error.
>By default, DEBUG=True but in production, please set it to False

**Settings for telegram bot:**
```python
31  BOT_TOKEN = 'bot token from @botfather'
32  AUTH_TOKEN = 'your token for authentication'
33  API_HASH = 'available in my.telegram.org'
34  API_ID = 'available in my.telegram.org'
35  ADMINS = ['IDs of admins to send messages']
```
* Bot token can be obtained from [@botfather](https://t.me/BotFather), just paste it here.
* AUTH_TOKEN can be any string you'd like. Its main purpose is to authenticate GET requests to an API. More info on `API Reference` section below.
* API_HASH and API_ID can be obtained from my.telegram.org. They are needed to communicate with telegram servers as Telethon [MTProto protocol](https://core.telegram.org/mtproto).
* ADMINS are the ones who can receive errors occured in your server. Just paste the ID number of them into the array. 
 
**Database settings:**
```python
88   DATABASES = {
89      'default': {
90          'ENGINE': 'django.db.backends.postgresql',
91          'NAME' : 'DB name',
92          'USER' : 'username',
93          'PASSWORD' : '12345678',
94          'HOST' : 'localhost',
95          'PORT' : 5432,
96      }
97   }
```
If you use PostgreSQL, please fill out database credentials. Django also supports MariaDB, MySQL, Oracle, SQLite. [More info](https://docs.djangoproject.com/en/5.0/ref/databases/) on how to configure them.


### API Reference
```http
  GET /api/?token=TOKEN&text=yourtext
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Your API key |
| `text` | `string` | **Required**. Text to send |
 Main purpose of this API is to inform any exceptions and errors occured in your other servers.You also can use it send texts messages. TOKEN should be the same as in `seetings.py` file. If correct, API will send the text to all admins.
 
 
### Deployment
After cloning, you have to create table in database. Run:
```bash
python manage.py makemigrations
``` 
This will create python files in migrations folder of each app. After run: 
```bash
python manage.py migrate
```
This will create tables in the database.

Normally, you create a superuser with ```python manage.py createsuperuser``` command to access Django admin panel. But if you want to create a default superuser, then run: 
```bash 
python manage.py seed
``` 
This will create a superuser with the usarname of 'admin' and password of 'PleaseChangeMe'.
>Don't forget to change your password after logging into the admin panel.

As Telethon is an asyncronous library, you have to run django project and telegram bot in seperate terminals:
```bash
python manage.py runserver
python manage.py run_bot
```


### Additional information
My project allows you to write documetation for your other products. Problem is that text editor which I implemented only works with videos links. So you have to first upload a video in `attachments` section of admin panel. Then copy its link in media folder and paste it in the text editor. This way you can include videos in your documentation.

For now, ticketing system only supports text messages. I will implement photo and video support later. Thanks!