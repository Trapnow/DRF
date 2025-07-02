from rest_framework.permissions import BasePermission, SAFE_METHODS


class PositionPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated or not user.role:
            return False

        role_perms = user.role.permissions.values_list("codename", flat=True)

        if request.method in SAFE_METHODS:
            return "view_question" in role_perms
        elif request.method == "POST":
            return "add_question" in role_perms
        elif request.method in ("PUT", "PATCH"):
            return "change_question" in role_perms
        elif request.method == "DELETE":
            return "delete_question" in role_perms

        return False
