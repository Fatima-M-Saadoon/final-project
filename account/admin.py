from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.forms import UserAdminChangeForm, UserAdminCreationForm
from account.models import User
from django.contrib.auth.models import Group

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'username','address1','phone_number','is_active', 'is_staff', 'is_superuser',)
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'user', 'username', 'phone_number', 'address1' )}),
        ('Permissions',
         {'fields': ( 'is_active', 'is_superuser', 'is_staff',  'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )
    search_fields = ('user', 'username')
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.site_header="لوحة التحكم "
admin.site.site_title="لوحة التحكم تطبيق هارمبو "
