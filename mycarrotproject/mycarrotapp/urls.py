from django.urls import path
from . import views

app_name = 'mycarrotapp'

urlpatterns = [
    path("", views.main, name="main"),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:pk>/', views.trade_post, name='trade_post'),
    path('write/', views.write, name='write'),
    path('create_form/', views.create_post, name='create_form'),
    path("chat/", views.chat, name="chat"),
    path("chat/<str:room_name>/<str:user_name>/", views.room, name="room"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
