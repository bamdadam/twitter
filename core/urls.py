from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from core import views

urlpatterns = [
    path('register', views.UserRegistration.as_view(), name='register'),
    path('get_auth_token/', obtain_auth_token, name='get_auth_token'),
    path('update_user/<int:id>/', views.UpdateSystemUser.as_view(), name='update_user'),
    path('create_tweet', views.CreateTweet.as_view(), name='create_tweet'),
    path('add_relationship', views.ListCreateRelationShip.as_view(), name='add_relationship'),
    path('list_system_users/', views.ListSystemUser.as_view(), name='list_system_users'),
    path('get_system_user/<int:pk>/', views.RetrieveSystemUser.as_view(), name='get_system_user'),
    path('list_add_relationship/', views.ListCreateRelationShip.as_view(), name='list_add_relationship'),
    path('delete_relationship/<int:pk>/', views.DeleteRelationShip.as_view(), name='delete_relationship'),
    path('tweet/<int:pk>/like/', views.LikeTweet.as_view(), name='like_tweet'),
    path('tweet/<int:pk>/unlike/', views.UnlikeTweet.as_view(), name='unlike_tweet'),
    path('tweet/<int:pk>/retweet/', views.RetweetTweet.as_view(), name='retweet_tweet'),
    path('timeline/', views.TimeLineTweets.as_view(), name='timeline_tweets'),
    path('systemuser_detail/', views.SystemUserDetail.as_view(), name='systemuser_detail'),
    # path('homepage/', views.HomePageTweets.as_view(), name='homepage_tweets')
]
