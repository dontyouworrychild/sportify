from rest_framework import permissions
from common.enums import SystemRoleEnum

class IsMe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.id == request.user.id
    
class IsOrganizator(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return SystemRoleEnum.ORGANIZATOR == request.user.role