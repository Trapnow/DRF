from rest_framework import permissions


class IsCompanyOwnerOrReadAndCreate(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_company_owner and request.user.company == obj
