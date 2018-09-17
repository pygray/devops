from rest_framework.routers import DefaultRouter
from .views import *

task_router = DefaultRouter()
task_router.register(r'tasks', TaskViewSet, base_name="tasks")
task_router.register(r'sys_task_list', SelectTaskViewSet, base_name="sys_task_list")
task_router.register(r'crontabs', CrontabViewSet, base_name="crontabs")
task_router.register(r'task_result', TaskResultViewSet, base_name="task_result")