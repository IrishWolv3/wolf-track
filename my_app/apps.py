from django.apps import AppConfig


class MyAppConfig(AppConfig): # This is the configuration class for the app.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_app'

    def ready(self): # This method is called when the app is ready.
        import my_app.signals