from django.urls import path
from . import views

app_name = 'mycarrotapp'

urlpatterns = [
    path("", views.main, name="main"),
    path("chat/", views.chat, name="chat"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
