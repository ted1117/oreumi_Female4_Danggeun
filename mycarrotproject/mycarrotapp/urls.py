from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path('trade_list/', views.trade_list, name='trade_list'),
    path('trade_post/', views.trade_post, name='trade_post'),
    path('write/', views.create_or_update_post, name='create_or_update_post'),
]
