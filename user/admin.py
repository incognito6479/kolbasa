from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from user.models import User, Deliver, Agent


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'user_type', 'user_region')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'fullname')
    ordering = ('username',)
    list_display = 'username', 'fullname', 'user_type', 'user_region',
    filter_horizontal = 'user_permissions',


admin.site.register(Deliver)
admin.site.register(Agent)
