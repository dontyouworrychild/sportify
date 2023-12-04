from django.shortcuts import get_object_or_404
from rest_framework import permissions
from student.models import Student
from coach.models import Coach
from common.enums import SystemRoleEnum

class IsPresident(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return SystemRoleEnum.PRESIDENT == request.user.role
    
class IsOrganizator(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return SystemRoleEnum.ORGANIZATOR == request.user.role
    

class IsCoach(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return SystemRoleEnum.COACH == request.user.role
    
class IsStudentCoach(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role != SystemRoleEnum.COACH:
            return False

        coach = get_object_or_404(Coach, id=request.user.id)

        student = request.data.get('student', None)

        return Student.objects.filter(id=student, coach=coach).exists()