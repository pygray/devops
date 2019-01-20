from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
   name = models.CharField("中文名", max_length=30, null=True)
   phone = models.CharField("手机", max_length=20, null=True)
   team = models.CharField("所属项目组", max_length=30, null=True)
   department = models.CharField("所属部门", max_length=30, null=True)

   def __str__(self):
       return self.username

   class Meta:
       verbose_name = "用户"
       permissions = (
           ("view_user", "查看用户"),
           ("add_user", "添加用户"),
           ("change_user", "修改用户"),
           ("delete_user", "删除用户")
       )
       db_table = "user_profile"
       ordering = ["id"]

   # def get_view_permissions(self):
   #     if self.is_superuser:
   #         return Menu.objects.all()
   #     return Menu.objects.filter(groups__in=self.groups.all())
