from __future__ import absolute_import, unicode_literals
from rest_framework import viewsets, response, status, mixins
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django_celery_results.models import TaskResult
from .models import TaskProfile, BatchTasks
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .filters import TaskFilter, TaskResultFilter, BacthTaskFilter
from celery import current_app
from .serializers import TaskSerializer, CrontabSerializer, TaskResultSerializer, BatchTasksSerializer
from scripts.ansible_api import ANSRunner
import json


class TaskViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定定时任务信息
    list:
        返回定时任务列表
    update:
        更新定时任务信息
    destroy:
        删除定时任务记录
    create:
        创建定时任务记录
    partial_update:
        更新定时部分字段
    """
    queryset = PeriodicTask.objects.all().order_by("-id")
    serializer_class = TaskSerializer
    filter_class = TaskFilter
    filter_fields = ("keywords",)

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.view_task_profile"):
            return super(TaskViewSet, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.view_taskprofile"):
            return super(TaskViewSet, self).retrieve(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def destroy(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.delete_taskprofile"):
            return super(TaskViewSet, self).destroy(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def create(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.add_taskprofile"):
            data = request.data
            name = data["name"]
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            TaskProfile(task_profile=PeriodicTask.objects.get(name=name), user=request.user).save()
            headers = self.get_success_headers(serializer.data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.change_taskprofile"):
            return super(TaskViewSet, self).update(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))


class CrontabViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定crontab表达式
    list:
        返回crontab表达式列表
    update:
        更新crontab表达式信息
    destroy:
        删除crontab表达式记录
    create:
        创建crontab表达式记录
    partial_update:
        更新crontab表达式部分字段
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions, )
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabSerializer

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.view_taskprofile"):
            return super(CrontabViewSet, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def create(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.add_taskprofile"):
            return super(CrontabViewSet, self).create(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.change_taskprofile"):
            return super(CrontabViewSet, self).update(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.view_taskprofile"):
            return super(CrontabViewSet, self).retrieve(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def destroy(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.delete_taskprofile"):
            return super(CrontabViewSet, self).destroy(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))




class TaskResultViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    """
    retrieve:
        返回指定定时任务执行结果
    list:
        返回定时任务执行结果列表
    destroy:
        删除执行结果记录记录
    """
    permission_classes = (IsAuthenticated, )
    queryset = TaskResult.objects.all().order_by("-id")
    serializer_class = TaskResultSerializer
    filter_class = TaskResultFilter
    filter_fields = ("keywords",)

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.view_taskprofile"):
            return super(TaskResultViewSet, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.view_taskprofile"):
            return super(TaskResultViewSet, self).retrieve(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    # 重写删除方法支持多个删除
    def destroy(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.delete_taskprofile"):
            ids = kwargs.get("pk")
            ids = ids.split(",")
            if ids and len(ids) == 1:
                task_result_obj = TaskResult.objects.get(pk=ids[0])
                self.perform_destroy(task_result_obj)
            elif len(ids) > 1:
                for id in ids:
                    task_result_obj = TaskResult.objects.get(pk=id)
                    self.perform_destroy(task_result_obj)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def perform_destroy(self, instance):
        instance.delete()


class SelectTaskViewSet(viewsets.ViewSet):

    """
    list:
        返回任务模板列表
    """

    celery_app = current_app
    permission_classes = (IsAuthenticated,)

    # permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("tasks.view_taskprofile"):
            data = self.get_task_data()
            return response.Response(data)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def get_task_data(self):
        current_app.loader.import_default_modules()
        # self.celery_app.loader.import_default_modules()
        tasks_list = list(sorted(name for name in self.celery_app.tasks
                          if not name.startswith('celery.')))
        t_list = [{"id": k+1, "name": v} for k, v in enumerate(tasks_list)]
        return t_list

class BatchTasksViewSet(viewsets.ModelViewSet):
    """
    create:
    创建任务
    list:
    获取热么列表
    retrieve:
    获取任务信息
    update:
    执行任务
    """
    permission_classes = (IsAuthenticated,)
    queryset = BatchTasks.objects.all()
    serializer_class = BatchTasksSerializer
    filter_class = BacthTaskFilter
    filter_fields = ("keywords", )
    def partial_update(self, request, *args, **kwargs):
        from datetime import datetime
        pk = int(kwargs.get("pk"))
        data = request.data
        user = request.user.username
        task = BatchTasks.objects.get(pk=pk)
        playbook_path = task.playbook.path
        rbt = ANSRunner()
        rbt.run_playbook(playbook_path)
        data['exec_time'] = datetime.now()
        data['user'] = user
        data['detail_result'] = json.dumps(rbt.get_playbook_result(), indent=4)
        BatchTasks.objects.filter(pk=pk).update(**data)
        return response.Response(status=status.HTTP_204_NO_CONTENT)













