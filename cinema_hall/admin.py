from django.contrib import admin

from cinema.admin import AdminInteractPermissionModelAdminMixin
from cinema_hall.models import Cinema, Hall

admin.site.register(
    Cinema,
    AdminInteractPermissionModelAdminMixin,
)

admin.site.register(
    Hall,
    AdminInteractPermissionModelAdminMixin,
)
