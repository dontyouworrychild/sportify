from rest_framework import permissions

class IsMe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.id == request.user.id