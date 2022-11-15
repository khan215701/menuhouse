from django.contrib import admin
from .models import User, profile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
  list_display = ('email', 'username', 'first_name', 'last_name', 'is_active')
  ordering = ('-date_joined',)
  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()

admin.site.register(User, CustomUserAdmin)
admin.site.register(profile)