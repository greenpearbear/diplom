from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    exclude = ['password']
    search_fields = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('last_login', 'date_joined')
