from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

from core.serializers import CreateSystemUserSerializer,UpdateSystemUserSerializer
from core.permissions import UpdateUserPermission
from core.models import SystemUser


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


# class HelloWorld(generics.GenericAPIView):
#     permissions = (permissions.IsAuthenticated,)
#
#     def get(self, request, *args, **kwargs):
#         return Response({'defailt': 'helloworld'})
