from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class TravelQuestAdminSite(admin.AdminSite):
    site_header = 'Monty Python administration'


ADMIN_SITE = TravelQuestAdminSite(name='travel_quest_admin')


@admin.register(User, site=ADMIN_SITE)
class TravelQuestUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "lvl",
        "is_staff", 
        "is_active",
    )
    search_fields = ("username",)
    list_filter = (
        "username",
        "email",
    )
    empty_value_display = "-пусто-"
