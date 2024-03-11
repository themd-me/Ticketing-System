from django.urls import path
from .views import cats, subs

urlpatterns = [
    path('', cats, name="docs"),
    path('<int:sub_id>/', subs),
]
