from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from .models import Organizator 

class OrganizatorAdmin(admin.ModelAdmin):
    exclude = ('role', 'is_staff', 'is_active', 'is_admin', 'last_login', 'groups', 'is_superuser', 'user_permissions')

    fieldsets = (
        (None, {"fields": ("username", "password", "phone_number", "first_name", "last_name", "image")}),
    )
    list_display = ("username", "phone_number", "first_name", "last_name", "image")

    def save_model(self, request, obj, form, change):
        obj.role = "organizator"
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Organizator, OrganizatorAdmin)
