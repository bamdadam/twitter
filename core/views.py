from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, JSONParser
from core.serializers import CreateSystemUserSerializer, UpdateSystemUserSerializer, CreateTweetSerializer, \
    RelationShipSerializer, GetTweetListSerializer
# Create your views here.


class UserRegistration(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CreateSystemUserSerializer
    parser_classes = (MultiPartParser, JSONParser,)