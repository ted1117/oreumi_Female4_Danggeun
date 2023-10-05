from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import set_region_certification

app_name = 'mycarrotapp'

urlpatterns = [
    path("", views.main, name="main"),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:pk>/', views.trade_post, name='trade_post'),
    path('write/', views.write, name='write'),
    path('create_form/', views.create_post, name='create_form'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('location/', views.location, name='location'),
    path('set_region/', views.set_region, name='set_region'),
    path('set_region_certification/', set_region_certification, name='set_region_certification'),
    path("chat/", views.chat, name="chat"),
    path("chat/<str:room_name>/<str:user_name>/", views.room, name="room"),
    path("chat/<int:post_id>/<str:viewer>/", views.get_or_create_room, name="get_or_create_room"),
    path('login/', views.login, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='mycarrotapp:main'), name='logout'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
]
