from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("chat/", views.chat, name="chat"),
    path("chat/<str:room_name>/", views.room, name="room"),
]
