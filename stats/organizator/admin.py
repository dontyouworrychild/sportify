from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Organizator

class OrganizatorAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password",)}),
        (_("Personal info"), {"fields": ("image", )}),
        (_("Role"), {"fields": ("role", )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", )}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "phone_number", "password1", "password2", "first_name", "last_name"),
            },
        ),
    )
    list_display = ("username", "phone_number", "first_name", "last_name", "is_staff")
    search_fields = ("username", "first_name", "last_name", "phone_number")

admin.site.register(Organizator, OrganizatorAdmin)
