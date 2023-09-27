from django.urls import path
from . import views

app_name = 'mycarrotapp'

urlpatterns = [
    path("", views.main, name="main"),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:pk>/', views.trade_post, name='trade_post'),
    path('write/', views.write, name='write'),
    path('create_form/', views.create_post, name='create_form'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('location/', views.location, name='location'),
    path("chat/", views.chat, name="chat"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
]
