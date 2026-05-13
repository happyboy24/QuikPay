from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from wallet.models import Transaction
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # list_display = ('first_name', 'last_name', 'email', 'phone', 'username')
    ...
    add_fieldsets = (
        (
            None, {
            "classes": ("wide",),
            "fields": ("username", "usable_password", "password1", "password2", "first_name", "last_name"),

        },
    ),

    )

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)





