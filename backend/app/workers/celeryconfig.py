from datetime import timedelta
from core.config import settings
from core.constants import *


broker_url = settings.CELERY_BROKER
result_backend = settings.CELERY_BACKEND

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']


# 导入任务所在文件
imports = [
    'workers.celery_tasks',
]

# 需要执行任务的配置
beat_schedule = {
    'test1': {
        'task': 'workers.celery_tasks.taskPrintDatetime',
        # 设置定时的时间
        'schedule': CELERY_PRINT_DATETIME,
        'args': ()
    }
}