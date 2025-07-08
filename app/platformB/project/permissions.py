from rest_framework import permissions
from .models import Storage


class IsCompanyOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_company_owner and request.user.company == obj


class IsRelatedToCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.company is not None

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'company'):
            return obj.company == request.user.company

        if hasattr(obj, 'storage'):
            return obj.storage.company == request.user.company

        return False