from asgiref.sync import sync_to_async
from System.settings import BOT_TOKEN
from Tickets.models import Ticket, Answer
from Bot.models import Theme, User
import requests


@sync_to_async #done
def get_lang(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        return user.language
    except:
        return 'uz'

@sync_to_async #done
def set_lang(user_id, lang):
    user = User.objects.get(user_id=user_id)
    user.language = lang
    user.save()

@sync_to_async  #done
def get_status(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        return user.status
    except:
        return "just started"

@sync_to_async  #done
def set_status(user_id, status):
    user = User.objects.get(user_id=user_id)
    user.status = status
    user.save()

@sync_to_async #done
def get_themes(user_id):
    themes = Theme.objects.all()
    lang = get_lang(user_id)
    if lang == 'uz':
        btns = [i.Uzbek_theme for i in themes]
    else:
        btns = [i.Russian_theme for i in themes]
    return btns

@sync_to_async #done
def save_theme(user_id, theme):
    user = User.objects.get(user_id=user_id)
    user.theme = theme
    user.save()

@sync_to_async
def open_ticket(event): #done
    user = User.objects.get(user_id=event.chat.id)
    user.opened_ticket = True
    user.save()
    
    ticket = Ticket(            
            theme = user.theme,
            message = event.message.text,
            user = user
            )
    ticket.save()

@sync_to_async
def opened_ticket(user_id):
    user = User.objects.get(user_id=user_id)
    return user.opened_ticket

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

def send_message(chat_id, text): #done
    server_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    params = {'chat_id' : chat_id, 'text' : text, 'parse_mode' : 'HTML'}
    requests.get(server_url, params=params)