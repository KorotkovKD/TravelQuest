from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Wallet


class TravelQuestAdminSite(admin.AdminSite):
    site_header = 'Monty Python administration'


ADMIN_SITE = TravelQuestAdminSite(name='travel_quest_admin')


@admin.register(User, site=ADMIN_SITE)
class TravelQuestUserAdmin(UserAdmin):

    fieldsets = (
        (None, {"fields": ("password", )}),
        (_("Personal info"), {"fields": ("first_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_confirmed",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = (
        "id",
        "email",
        "photo",
        "bio",
        "is_staff",
        "is_active",
        "is_confirmed",
    )
    search_fields = ("email",)
    list_filter = (
        "is_staff",
        "is_active",
    )
    empty_value_display = "-пусто-"


@admin.register(Wallet, site=ADMIN_SITE)
class TravelQuestWalletAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "value",
    )
    search_fields = ("owner",)
    empty_value_display = "-пусто-"
