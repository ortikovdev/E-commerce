from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserToken
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'full_name', 'is_superuser', 'is_staff', 'is_active', 'modified_date', 'created_date')
    readonly_fields = ('last_login', 'modified_date', 'created_date')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    date_hierarchy = 'created_date'
    ordering = ()
    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('modified_date', 'created_date')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2'), }),
    )
    search_fields = ('email', 'full_name')


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token', 'created_date')
    date_hierarchy = 'created_date'
    search_fields = ('user__username', 'user_full_name', 'token')


admin.site.register(User, UserAdmin)

admin.site.index_title = _('Ecommerce administration')
admin.site.site_header = _('Ecommerce')