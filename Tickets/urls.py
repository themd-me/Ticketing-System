from django.urls import path
from .views import edit, answers, submit

urlpatterns = [
    path('<int:ticket_id>/', edit),
    path('<int:ticket_id>/answers', answers),
    path('<int:ticket_id>/submit', submit)
]
