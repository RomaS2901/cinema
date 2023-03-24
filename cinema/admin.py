from django.contrib.admin import ModelAdmin


class AdminInteractPermissionModelAdminMixin(
    ModelAdmin,
):
    def has_add_permission(
        self,
        request,
    ):
        return request.user.is_superuser

    def has_view_or_change_permission(
        self,
        request,
        obj=None,
    ):
        return request.user.is_superuser

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):
        return request.user.is_superuser
