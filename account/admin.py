from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ("groups", "user_permissions")
    list_filter = ("is_active", "is_admin", 'is_staff')
    fieldsets = (
        ('Personal', {'fields': ('username', 'first_name', 'last_name', 'password', 'must_change_password')}),
        ('Permissions', {'fields': ('is_staff', 'is_admin', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Account information', {'fields': readonly_fields})
    )
    add_fieldsets = (
        ('Personal', {'fields': ('username', 'first_name', 'last_name', 'password1', 'password2', 'must_change_password')}),
        ('Permissions', {'fields': ('is_staff', 'is_admin', 'is_active', 'is_superuser', 'groups', 'user_permissions')})
    )


admin.site.register(Account, AccountAdmin)
