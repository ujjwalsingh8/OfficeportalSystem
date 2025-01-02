from django.apps import AppConfig


class UserManagmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_managment'
    

    def ready(self):
        import user_managment.signals