# users/admin.py  (or whatever app your CustomUser lives in)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # -------------------------
    # List page (table)
    # -------------------------
    list_display = (
        "id",
        "email",
        "username",
        "user_type",
        "branch",
        "is_staff",
        "is_active",
        "profile_preview",
        "last_login",
        "date_joined",
    )
    list_filter = ("user_type", "branch", "is_staff", "is_active", "is_superuser")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)

    # -------------------------
    # Detail page (edit form)
    # -------------------------
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("username", "first_name", "last_name", "profile", "user_type", "branch")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "user_type",
                    "branch",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    readonly_fields = ("profile_preview", "last_login", "date_joined")

    # -------------------------
    # UX: show profile thumbnail
    # -------------------------
    @admin.display(description="Profile")
    def profile_preview(self, obj):
        if obj.profile:
            return format_html(
                '<img src="{}" style="height:32px;width:32px;border-radius:50%;object-fit:cover;" />',
                obj.profile.url,
            )
        return "—"
