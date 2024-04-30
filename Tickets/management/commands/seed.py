from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates default super user.'

    def handle(self, *args, **options): 
        if not User.objects.filter(username='admin').exists():
            # Create superuser
            User.objects.create_superuser('admin', 'ask.md@telegmail.com', 'PleaseChangeMe')
            print('Superuser created successfully.')
        else:
            print('Superuser already exists.')