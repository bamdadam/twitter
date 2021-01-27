from rest_framework import permissions

from core.models import SystemUser


class UpdateUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            system_user = SystemUser.objects.get(id=view.kwargs['id'])
            # print(view.kwargs['id'])
            # print(system_user.user)
            # print(request.user)
            return bool(system_user.user == request.user)
        except (SystemUser.DoesNotExist, KeyError, ValueError):
            return False
