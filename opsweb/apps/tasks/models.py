from __future__ import unicode_literals

from django.db import models

from cmdb.models import Server
from django_celery_beat.models import PeriodicTask
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskProfile(models.Model):
    task_profile = models.OneToOneField(PeriodicTask, related_name="task_profile", on_delete=models.CASCADE, help_text="PeriodicTask添加字段")
    user = models.CharField("执行用户", max_length=50, null=True, help_text="执行用户")
    server = models.ForeignKey(Server, verbose_name="服务器", null=True, help_text="服务器")

    def __str__(self):
        return self.task_profile

    class Meta:
        verbose_name = "task任务衍生表"
        permissions = (
            ("view_task_profile", "cat view task_profile"),
        )
        db_table = "task_profile"
        ordering = ["id"]

class BatchTasks(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'任务名称')
    playbook = models.FileField(upload_to='playbook/%Y/%m', verbose_name=u'playbook文件')
    detail_result = models.TextField(verbose_name=u'执行结果详情',null=True, blank=True)
    status = models.CharField(max_length=1, choices=(('Y', '已执行'), ('N', '未执行')), default='N', verbose_name='执行状态')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'任务创建时间')
    exec_time = models.DateTimeField(auto_now=True, verbose_name=u'执行时间')

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("view_batchTask", "cat view batchTask"),
        )
        verbose_name = '批量任务'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']


