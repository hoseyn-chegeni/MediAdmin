from django.apps import AppConfig


class ReceptionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reception"

    def ready(self):
        from .signals import update_last_reception_date, update_reception_number, send_sms
