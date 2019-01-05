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
       verbose_name = "用户表"
       permissions = (
           ("view_user", "cat view user"),
       )
       db_table = "user_profile"
       ordering = ["id"]

   # def get_view_permissions(self):
   #     if self.is_superuser:
   #         return Menu.objects.all()
   #     return Menu.objects.filter(groups__in=self.groups.all())
