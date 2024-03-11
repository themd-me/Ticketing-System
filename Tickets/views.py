from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Ticket, Answer
from Bot.functions import send_message
from Bot.models import User

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        ticket_number = Ticket.objects.filter(is_open=True)
        return render(request, 'index.html', {'number' : len(ticket_number)})
    else:
        return redirect('login')
        
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'message' : 'Invalid login credentials. Please try again...'})
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'login.html', {})

def user_logout(request):
    logout(request)
    return redirect('login')

def tickets(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.all()
        return render(request, 'tickets.html', { 'tickets' : tickets})
    else:
        return redirect('login')

def edit(request, ticket_id):
    if request.user.is_authenticated:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.visited = True
        ticket.save()
        return render(request, 'edit.html', { 'ticket' : ticket })
    else:
        return redirect('login')

def answers(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    answers = Answer.objects.filter(ticket_id=ticket_id)
    return render(request, 'answers.html', { 'answers' : answers, 'ticket' : ticket })
       
def submit(request, ticket_id):
     if request.method == "POST" and request.user.is_authenticated:
        message = request.POST['message']
        is_open = request.POST.get('is_open')
        user_id = request.POST['user_id']

        ticket = Ticket.objects.get(id=ticket_id)

        user = User.objects.get(user_id=user_id)

        
        if is_open == 'closed':
            ticket.is_open = False
            user.opened_ticket = False
            user.status = 'pressed start'
            if message == '':
                message = '<b>Ticket yopildi!</b>'
                send_message(user_id, message)
            else:
                send_message(user_id, f'<b>Admindan javob:</b>\n\n{message}\n\n<b>Ticket yopildi!</b>')
        else:
            send_message(user_id, f'<b>Admindan javob:</b>\n\n{message}')

        answer = Answer(
                        ticket_id = ticket,
                        message = message,
                        by_whom = request.user.first_name
                    )

        ticket.save()
        user.save()
        answer.save()

        return answers(request, ticket_id)