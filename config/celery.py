import os

import dotenv
from celery import Celery

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
dotenv.read_dotenv(env_file)
# Задаем переменную окружения, содержащую название файла настроек нашего проекта.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app = Celery('config')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

