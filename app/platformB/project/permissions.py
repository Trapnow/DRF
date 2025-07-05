from rest_framework import permissions
from .models import Storage


class IsCompanyOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_company_owner and request.user.company == obj


class IsRelatedToCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        storage_pk = view.kwargs.get('pk')

        if not storage_pk:
            return True

        try:
            storage = Storage.objects.get(pk=storage_pk)
            return request.user.company == storage.company
        except Storage.DoesNotExist:
            return False