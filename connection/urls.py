from django.urls import path
from . import views

urlpatterns = [
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/', views.accept_friend_request, name='accept_friend_request'),
    path('pending_requests/', views.check_pending_requests, name='check_pending_requests'),
    path('sent_requests/', views.check_sent_requests, name='check_sent_requests'),
    path('reject_friend_request/', views.reject_friend_request, name='reject_friend_request'),
    path('check_friends/', views.check_friends, name='check_friends'),
]