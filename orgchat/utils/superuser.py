from django.http import JsonResponse
from rest_framework.permissions import BasePermission

def superuser_required_json(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return JsonResponse({'error': 'Forbidden'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
