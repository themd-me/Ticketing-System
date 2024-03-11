from django.contrib import admin
from .models import Theme, User, Exception

# Register your models here.

admin.site.register(Theme)
admin.site.register(User)
admin.site.register(Exception)