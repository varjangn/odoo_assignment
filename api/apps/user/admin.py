from django.contrib import admin
from apps.user.models import UserSession


class UserSessionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "login_time"
    )


admin.site.register(UserSession, UserSessionAdmin)
