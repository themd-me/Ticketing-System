from django.db import models
from Bot.models import User

# Create your models here.

class Ticket(models.Model):
    theme = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class Answer(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    by_whom = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message