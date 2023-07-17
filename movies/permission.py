from rest_framework.views import Request

from rest_framework import permissions

class AnyUserOrEmployee(permissions.BasePermission):
  def has_permission(self, request: Request, view):
      if request.method in permissions.SAFE_METHODS:
          return True
      return request.user.is_superuser and request.user.is_authenticated