from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'role',
        'is_active',
        'created_at',
    )

    list_filter = (
        'role',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'phone_number',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'POS Information',
            {
                'fields': (
                    'role',
                    'phone_number',
                    'profile_picture',
                    'is_active_staff',
                )
            }
        ),
    )