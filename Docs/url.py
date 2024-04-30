from django.urls import path
from .views import cats, subs, redirect_docs

urlpatterns = [
    path('', redirect_docs, name="docs"),
    path('<str:locale>/', cats, name="locale"),
    path('<str:locale>/<int:sub_id>/', subs),
]