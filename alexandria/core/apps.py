from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string


class DefaultConfig(AppConfig):
    name = "alexandria.core"
    label = "alexandria_core"

    def ready(self):
        # to avoid recursive import error, load extension classes
        # only once the app is ready
        from .models import VisibilityMixin, PermissionMixin
        from .serializers import BaseSerializer

        PermissionMixin.permission_classes = [
            import_string(cls) for cls in settings.PERMISSION_CLASSES
        ]
        VisibilityMixin.visibility_classes = [
            import_string(cls) for cls in settings.VISIBILITY_CLASSES
        ]

        BaseSerializer.validation_classes = [
            import_string(cls) for cls in settings.VALIDATION_CLASSES
        ]
