from django.contrib import admin
from django.contrib.auth.models import Group
from authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_of_creation', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('username', 'email', )
    list_filter = ('date_of_creation', )
    search_fields = ('username__startswith', 'email__startswith', )
    readonly_fields = ('date_of_creation', )
    fields = ('email', 'username', 'image', 'last_login', 'date_of_creation', 'is_active')


admin.site.unregister(Group)
