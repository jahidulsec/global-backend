from rest_framework import permissions


class IsManagerOnly(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user
        if user.groups.filter(name="Manager").exists():
            return True
        else:
            return False