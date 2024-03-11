from django.core.management.base import BaseCommand
from Bot.bot import bot

class Command(BaseCommand):
    help = 'Runs the bot until disconnected'

    def handle(self, *args, **options):
        bot.run_until_disconnected()