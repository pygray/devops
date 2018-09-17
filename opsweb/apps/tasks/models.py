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


