from asgiref.sync import sync_to_async
from System.settings import BOT_TOKEN, ALLOWED_HOSTS
from Tickets.models import Ticket, Answer
from Docs.models import Category, Subcategory
from Bot.models import Theme, User, Exception
import requests

@sync_to_async
def exceptions():
    exception = []
    themes = Theme.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    exception_class = Exception.objects.all()

    for the in themes:
        exception.append(the.themes)
    for cat in categories:
        exception.append(cat.category)
    for sub in subcategories:
        exception.append(sub.title)
    for ex in exception_class:
        exception.append(ex.item)

    return exception

@sync_to_async
def language(event):
    user = User.objects.get(user_id=event.chat.id)
    txt = event.message.text
    if txt == "O'zbek":
        user.language = 'UZ'
    elif txt == 'Русский':
        user.language = 'RU'
    else:
        user.language = 'EN'
    user.save()

@sync_to_async
def get_link(txt):
    subs = Subcategory.objects.all()
    for sub in subs:
        if txt == sub.title:
            return f'http://{ALLOWED_HOSTS[0]}:8000/docs/{sub.id}/'
    return 'No link'

@sync_to_async
def get_subs(txt):
    subcat = Subcategory.objects.filter(category__category=txt)
    subs = [i.title for i in subcat]
    return subs

@sync_to_async
def get(txt):
    if txt == 'buttons':
        themes = Theme.objects.all()
        btns = [i.themes for i in themes]
        return btns
    elif txt == 'categories':
        categories = Category.objects.all()
        cats = [i.category for i in categories]
        return cats

@sync_to_async
def save_ticket(event, user):
    ticket = Ticket(            
            theme = user.theme,
            message = event.message.text,
            user = user
            )
    user.opened_ticket = True
    user.save()
    ticket.save()

@sync_to_async
def save_user(event):
    user = User.objects.filter(user_id=event.chat.id)
    if len(user) == 0:
        user = User(
            status = 'pressed start',
            user_id = event.chat.id,
            first_name = event.chat.first_name,
            last_name = event.chat.last_name
        )
        user.save()

@sync_to_async
def get_user(id):
    try:
        user = User.objects.get(user_id=id)
        return user
    except DoesNotExist:   
        print('User not found')

@sync_to_async
def save(what, id, txt):
    user = User.objects.get(user_id=id)
    if what == 'status':
        user.status = txt
    elif what == 'theme':
        user.theme = txt
    user.save()

@sync_to_async
def save_answer(event):
    ticket = Ticket.objects.filter(user__user_id=event.chat.id, is_open=True).first()
    ticket.visited = False
    answer = Answer(
        ticket_id = ticket,
        message = event.message.text,
        by_whom = 'user'
    )
    ticket.save()
    answer.save()

def send_message(chat_id, text):
    server_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    params = {'chat_id' : chat_id, 'text' : text, 'parse_mode' : 'HTML'}
    requests.get(server_url, params=params)
