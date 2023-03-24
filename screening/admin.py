from django.contrib import admin

from cinema.admin import AdminInteractPermissionModelAdminMixin
from screening.models import Movie


admin.site.register(
    Movie,
    AdminInteractPermissionModelAdminMixin,
)
