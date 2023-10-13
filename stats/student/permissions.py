from rest_framework import permissions
from common.enums import SystemRoleEnum
from .models import Student
from coach.models import Coach
from django.shortcuts import get_object_or_404

class IsStudentCoach(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        coach = get_object_or_404(Coach, id=request.user.id)
        student_id = view.kwargs.get('pk')

        return Student.objects.filter(id=student_id, coach=coach).exists()

class IsCoach(permissions.BasePermission):
    def has_object_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return SystemRoleEnum.COACH in request.user.role
    
