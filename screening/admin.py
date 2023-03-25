from django.contrib import admin

from cinema.admin import AdminInteractPermissionModelAdminMixin
from screening.models import Movie, ScreeningSession

admin.site.register(
    Movie,
    AdminInteractPermissionModelAdminMixin,
)
admin.site.register(
    ScreeningSession,
    AdminInteractPermissionModelAdminMixin,
)
