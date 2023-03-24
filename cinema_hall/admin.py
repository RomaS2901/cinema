from django.contrib import admin

from cinema.admin import AdminInteractPermissionModelAdminMixin
from cinema_hall.models import Cinema

admin.register(
    Cinema,
    AdminInteractPermissionModelAdminMixin,
)
