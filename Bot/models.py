from django.db import models

# Create your models here.

class Theme(models.Model):
    themes = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.themes

class User(models.Model):
    languages = (
        ('UZ', "O'zbek"),
        ('RU', 'Русский'),
        ('EN', 'English'),
    )
    
    language = models.CharField(max_length=2, choices=languages, default='UZ')
    opened_ticket = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default='Unavailable')
    theme = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

class Exception(models.Model):
    item = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.item