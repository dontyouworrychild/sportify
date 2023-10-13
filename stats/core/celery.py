from django.apps import apps, AppConfig
from django.conf import settings
import os
from celery import Celery

if not settings.configured:
    # environment = config('ENVIRONMENT')
    environment = os.environ.get('ENVIRONMENT')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "core.settings."+environment) 

APP = Celery('core')


class CeleryConfig(AppConfig):
    name = 'core'
    verbose_name = 'Celery Config'

    def ready(self):
        APP.config_from_object('django.conf:settings', namespace='CELERY')
        APP.conf.broker_url = settings.CELERY_BROKER_URL
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        APP.autodiscover_tasks(installed_apps, force=True)