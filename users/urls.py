from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('user/', views.user_details, name='user_details'),
    path('search/', views.search_users, name='search_users'),
]
