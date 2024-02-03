# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_school_user', 'is_government_user', 'is_staff','state','is_district_user','is_approved', 'District','is_superuser','s_category')
    list_filter = ('is_school_user', 'is_government_user','is_district_user', 'is_approved','is_staff', 'is_superuser','state','District','s_category')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email','state','District')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('User Type', {'fields': ('is_school_user', 'is_government_user','is_district_user','is_approved','s_category')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
