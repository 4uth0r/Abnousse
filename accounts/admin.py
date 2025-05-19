from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(CustomUser)
class CustomUser(UserAdmin):
    inlines = [ProfileInline]
