from rest_framework.permissions import BasePermission

class AuthenticatedUser(BasePermission):
  def has_object_permission(self, request, view, obj):
      if request.user == obj:
          return True
