from django.shortcuts import render
from .models import Category, Subcategory

# Create your views here.

def cats(request):
    cats = Category.objects.all()
    subs = Subcategory.objects.all()
    return render(request, 'cats.html', { 'cats' : cats, 'subs' : subs })

def subs(request, sub_id):
    subs = Subcategory.objects.get(id=sub_id)
    return render(request, 'subs.html', { 'subs' : subs })