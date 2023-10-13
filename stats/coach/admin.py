from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Coach


# class CoachAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {"fields": ("username", "password",)}),
#         (_("Personal info"), {"fields": ("image", "first_name", "last_name", )}),
#         (_("Sport"), {"fields": ("club", "location", )}),
#         (_("Role"), {"fields": ("role", )})
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("username", "first_name", "last_name", "phone_number", "password1", "password2", "club", "location"),
#             },
#         ),
#     )
#     list_display = ("username", "first_name", "last_name", "last_login", )
#     search_fields = ("username", "first_name", "last_name", )

# admin.site.register(Coach, CoachAdmin)
admin.site.register(Coach)
