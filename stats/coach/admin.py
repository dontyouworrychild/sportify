from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from .models import Coach 

class CoachAdmin(admin.ModelAdmin):
    exclude = ('role', 'is_staff', 'is_active', 'is_admin', 'last_login', 'groups', 'is_superuser', 'user_permissions')

    fieldsets = (
        (None, {"fields": ("username", "password", "phone_number", "first_name", "last_name", "image", "club")}),
    )
    list_display = ("username", "phone_number", "first_name", "last_name", "image", "club")

    def save_model(self, request, obj, form, change):
        obj.role = "coach"
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Coach, CoachAdmin)
