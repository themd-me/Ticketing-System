from .functions import send_message
from System.settings import AUTH_TOKEN, ADMINS
from django.http import JsonResponse


def api(request):
    if request.method == 'GET':
        token = request.GET['token']
        if token:
            if token == AUTH_TOKEN:
                text = request.GET['text']
                for i in ADMINS:
                    send_message(i, text)
                return JsonResponse({'OK': 'True'})
            else:
                return JsonResponse({'Error': 'Invalid token'} )
        else:
            return JsonResponse({'Error': 'Token not found'})