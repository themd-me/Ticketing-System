from django.shortcuts import render, redirect
from .models import Category, Subcategory
from django.utils.translation import activate, gettext as _

# Create your views here.

def redirect_docs(request):
    return redirect('locale', locale='uz')

def cats(request, locale):  
    activate(locale)

    cats = Category.set_locale(Category, locale).objects.all()
    subs = Subcategory.set_locale(Subcategory, locale).objects.all()

    docs = _('docs')
    return render(request, 'cats.html', { 'cats' : cats, 'subs' : subs, 'docs' : docs })

def subs(request, sub_id, locale):
    sub = Subcategory.set_locale(Subcategory, locale).objects.get(id=sub_id)
    cat = Category.set_locale(Category, locale).objects.get(id=sub.linked_category.id)
    return render(request, 'subs.html', { 'sub' : sub, 'cat' : cat })