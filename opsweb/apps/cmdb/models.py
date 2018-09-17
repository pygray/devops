from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# from users.models import UserProfile


# Create your models here.


class Idc(models.Model):
    """
    厂商模型
    """
    name = models.CharField("厂商名称", max_length=32, db_index=True, unique=True, help_text="厂商名称")
    address = models.CharField("厂商地址", max_length=256, default="null", help_text="厂商地址")
    phone = models.CharField("厂商对接人电话", max_length=15, default="null", help_text="厂商对接人电话")
    email = models.EmailField("厂商对接人邮箱地址", default="null", help_text="厂商对接人邮箱地址")
    letter = models.CharField("厂商简称", max_length=30, db_index=True, unique=True, default="null", help_text="厂商简称")
    remark = models.CharField("备注说明", max_length=255, null=True, blank=True, help_text="备注说明")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "厂商表"
        permissions = (
            ("view_idc", "cat view idc"),
        )
        db_table = "resource_idc"
        ordering = ["id"]


class Env(models.Model):
    """
    环境模型
    """
    name = models.CharField("环境名称", max_length=50, db_index=True, unique=True, help_text="环境名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "环境表"
        db_table = "resource_env"
        permissions = (
            ("view_env", "cat view env"),
        )
        ordering = ["id"]


class Product(models.Model):
    name = models.CharField("项目名称", max_length=32, help_text="项目名称")
    pid = models.IntegerField("上级业务线id", db_index=True, default=0, help_text="上级业务线id")
    product_interface = models.ManyToManyField(User, verbose_name="项目接口人", related_name="product_interface", help_text="项目接口人")
    dev_interface = models.ManyToManyField(User, verbose_name="开发接口人", related_name="dev_interface", help_text="开发接口人")
    ops_interface = models.ManyToManyField(User, verbose_name="运维接口人", related_name="ops_interface", help_text="运维接口人")
    idc = models.ManyToManyField(Idc, verbose_name="所属厂商", related_name='product_idc', help_text="所属厂商")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'resource_product'
        permissions = (
            ("view_product", "can view products"),
        )
        ordering = ["id"]


class Server(models.Model):
    """
    服务器模型
    """
    hostname = models.CharField("主机名", max_length=50, db_index=True, unique=True, help_text="主机名")
    idc = models.ForeignKey(Idc, related_name="idc", verbose_name="主机对应的idc", help_text="主机对应IDC")
    InstanceId = models.CharField("实例ID", max_length=150, default="null", db_index=True, help_text="实例ID")
    ip = models.CharField("IP地址", max_length=100, default="null", db_index=True, help_text="IP地址")
    cpu = models.CharField("cpu核数", max_length=10, help_text="cpu核数", default="null")
    memory = models.CharField("内存", max_length=30, help_text="内存", default="null")
    status = models.CharField("服务器状态", max_length=32, default="初始", db_index=True, help_text="服务器状态")
    env = models.ForeignKey(Env, related_name="env", verbose_name="所属环境", null=True, help_text="所属环境")
    product = models.ForeignKey(Product, related_name="server_product", verbose_name="项目", null=True, help_text="所属项目")
    service = models.ForeignKey(Product, related_name="server_service", verbose_name="服务", null=True, help_text="所属服务")
    os = models.CharField("系统", max_length=100, db_index=True, default="null", help_text="系统")
    LastCheck = models.DateTimeField("检测时间", db_index=True, auto_now=True, help_text="检测时间")
    remark = models.CharField("服务器备注", max_length=300, default="null", help_text="服务器备注")

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = "服务器表"
        db_table = "resource_server"
        permissions = (
            ("view_server", "cat view server"),
        )
        ordering = ["id"]
#
#
# class Disk(models.Model):
#     """
#     磁盘模型
#     """
#     server = models.ForeignKey(Server, verbose_name="对应的server", help_text="所在server")
#     InstanceId = models.CharField("服务器ID", max_length=100, null=True, help_text="服务器ID")
#     disk = models.CharField("磁盘ID/name", max_length=100, null=True, help_text="磁盘ID/name")
#     device = models.CharField("磁盘挂载路径", default="null", max_length=50, help_text="磁盘挂载路径")
#     DiskSize = models.CharField("磁盘大小", max_length=50, help_text="磁盘大小")
#     LastCheck = models.DateTimeField("检测时间", db_index=True, auto_now=True, help_text="检测时间")
#     remark = models.CharField("磁盘备注", max_length=300, default="null", help_text="磁盘备注")
#
#     def __str__(self):
#         return self.device
#
#     class Meta:
#         verbose_name = "磁盘表"
#         db_table = "disk"
#         ordering = ["id"]
#
#
