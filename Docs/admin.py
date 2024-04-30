from django.contrib import admin
from .models import Category, Subcategory
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class SubAdmin(SummernoteModelAdmin):
    summernote_fields = ['Uzbek_body', 'Russian_body']

admin.site.register(Category)
admin.site.register(Subcategory, SubAdmin)