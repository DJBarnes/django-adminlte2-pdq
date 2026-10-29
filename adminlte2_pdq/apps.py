"""Django AdminLTE2 app configuration."""

# Third-Party Imports.
from django.apps import AppConfig


class AdminLte2PdqConfig(AppConfig):
    """App configuration. Registers the package's system checks."""

    name = "adminlte2_pdq"
    verbose_name = "Django AdminLTE2 PDQ"

    def ready(self):
        # Importing the module registers its checks (Django's documented pattern for system checks).
        from adminlte2_pdq import checks  # noqa: F401, PLC0415
