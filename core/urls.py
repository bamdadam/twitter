from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from core import views

urlpatterns = [
    path('register', views.UserRegistration.as_view(), name='register'),
    path('get_auth_token/', obtain_auth_token, name='get_auth_token'),
    path('update_user/<int:id>/',
         views.UpdateSystemUser.as_view(), name='update_user'),
    path('create_tweet/', views.CreateTweet.as_view(), name='create_tweet'),
    # path('add_relationship', views.AddRelationShip.as_view(), name='add_relationship'),
]
