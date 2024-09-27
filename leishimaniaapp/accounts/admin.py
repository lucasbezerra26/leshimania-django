from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass
