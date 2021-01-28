from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

from core.serializers import CreateSystemUserSerializer, UpdateSystemUserSerializer, CreateTweetSerializer, \
    RelationShipSerializer, DjangoUserSerializer, SystemUserSerializer, TweetSerializer

from core.permissions import UpdateUserPermission
from core.models import SystemUser, Tweet, Event, RelationShip


# Create your views here.


class UserRegistration(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CreateSystemUserSerializer
    parser_classes = (MultiPartParser, JSONParser,)


class UpdateSystemUser(generics.UpdateAPIView):
    permission_classes = [UpdateUserPermission, ]
    serializer_class = UpdateSystemUserSerializer
    parser_classes = (MultiPartParser, JSONParser,)

    def get_object(self):
        return get_object_or_404(SystemUser, id=self.kwargs["id"])


class CreateTweet(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CreateTweetSerializer

    def perform_create(self, serializer):
        serializer.save(original_owner=self.request.user.systemuser)


class UnlikeTweet(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, id=kwargs['pk'])
        tweet.like_count -= 1
        tweet.liked_by.remove(self.request.user.systemuser)
        tweet.save()
        return Response({'detail': 'unliked successfully'}, status=status.HTTP_200_OK)


class LikeTweet(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, id=kwargs['pk'])
        tweet.like_count += 1
        tweet.liked_by.add(self.request.user.systemuser)
        tweet.save()
        Event.objects.create(second_user=self.request.user.systemuser, owner=tweet.original_owner,
                             event_type=Event.liked_tweet)
        return Response({'detail': 'liked successfully'}, status=status.HTTP_200_OK)


class ListCreateRelationShip(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = RelationShipSerializer

    def get_queryset(self):
        return RelationShip.objects.filter(first_user=self.request.user.systemuser)

    def perform_create(self, serializer):
        serializer.save(first_user=self.request.user.systemuser)


class ListSystemUser(generics.ListAPIView):
    permissions_classes = (permissions.IsAuthenticated,)
    queryset = SystemUser.objects.all()
    serializer_class = SystemUserSerializer


class RetrieveSystemUser(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = SystemUser.objects.all()
    serializer_class = SystemUserSerializer


class DeleteRelationShip(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SystemUserSerializer

    def get_queryset(self):
        return RelationShip.objects.filter(first_user=self.request.user.systemuser)


class RetweetTweet(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, id=kwargs['pk'])
        user = self.request.user.systemuser
        user.retweeted_tweets.add(tweet)
        user.save()
        return Response({'detail': 'retweeted successfully'}, status=status.HTTP_200_OK)


class UndoRetweetTweet(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, id=kwargs['pk'])
        user = self.request.user.systemuser
        user.retweeted_tweets.remove(tweet)
        user.save()
        return Response({'detail': 'undo retweet successful'})


class TimeLineTweets(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TweetSerializer

    @staticmethod
    def get_following_tweets(following):
        return following.owned_tweets.all() | following.retweeted_tweets.all()

    def get_queryset(self):
        # print("fuck")
        user = self.request.user.systemuser
        relationships = RelationShip.objects.filter(first_user=user)
        # print(relationships)
        all_tweets = None
        for rel in relationships:
            following = rel.second_user
            if all_tweets is None:
                all_tweets = self.get_following_tweets(following)
            else:
                all_tweets = all_tweets | self.get_following_tweets(following)
        return all_tweets


class SystemUserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SystemUserSerializer
    queryset = SystemUser.objects.all()

    def get_object(self):
        return self.request.user.systemuser


class RetrieveTweet(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

# class HomePageTweets(generics.ListAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = TweetSerializer
#
#     def get_queryset(self):
#         all_tweets = list()
#         owned_tweets = self.request.user.systemuser.owned_tweets.all()
#         ret_tweets = self.request.user.systemuser.retweeted_tweets.all()
#         if owned_tweets:
#             all_tweets.append(owned_tweets)
#         if ret_tweets:
#             all_tweets.append(ret_tweets)
#         return all_tweets
