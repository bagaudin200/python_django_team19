import os
import environ
from celery import Celery

# Задаем переменную окружения, содержащую название файла настроек нашего проекта.
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
environ.Env.read_env(env_file)

celery_app = Celery('config')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
