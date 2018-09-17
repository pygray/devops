from rest_framework import serializers
from .models import *


# class IdcSerialiser(serializers.Serializer):
#     """
#     Idc 序列化类
#     """
#
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(required=True, max_length=32, help_text="idc名称", label="idc名称",
#                                     error_messages={"blank": "机房名称不能为空",
#                                                     "required": "这个字段为必要字段"
#                                                     })
#     IdcAddress = serializers.CharField(required=True, max_length=256, help_text="idc地址", label="idc地址",
#                                        error_messages={"blank": "地址不能为空",
#                                                        "required": "这个字段为必要字段"
#                                                        })
#     phone = serializers.CharField(required=True, max_length=15, help_text="联系电话", label="联系电话",
#                                   error_messages={"blank": "联系电话不能为空",
#                                                   "required": "这个字段为必要字段"
#                                                   })
#     email = serializers.EmailField(required=True, help_text="邮箱", label="邮箱", error_messages={"blank": "邮箱不能为空",
#                                                                                               "required": "这个字段为必要字段"
#                                                                                               })
#     IdcLetter = serializers.CharField(required=True, max_length=30, help_text="idc简称", label="idc简称",
#                                       error_messages={"blank": "idc简称不能为空",
#                                                       "required": "这个字段为必要字段"
#                                                       })
#
#     def create(self, validated_data):
#         return Idc.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.IdcName = validated_data.get("name", instance.IdcName)
#         instance.IdcAddress = validated_data.get("IdcAddress", instance.IdcAddress)
#         instance.phone = validated_data.get("phone", instance.phone)
#         instance.email = validated_data.get("email", instance.email)
#         instance.IdcLetter = validated_data.get("IdcLetter", instance.IdcLetter)
#         instance.save()
#         return instance


class IdcSerializer(serializers.ModelSerializer):
    """
    厂商序列化
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=32, help_text="厂商名称", label="厂商名称",
                                 error_messages={"blank": "名称不能为空",
                                                 "required": "这个字段为必要字段"
                                                 })
    address = serializers.CharField(required=True, max_length=256, help_text="厂商地址", label="厂商地址",
                                    error_messages={"blank": "地址不能为空",
                                                    "required": "这个字段为必要字段"
                                                    })
    phone = serializers.CharField(required=True, max_length=15, help_text="联系电话", label="联系电话",
                                  error_messages={"blank": "联系电话不能为空",
                                                  "required": "这个字段为必要字段"
                                                  })
    email = serializers.EmailField(required=True, help_text="邮箱", label="邮箱", error_messages={"blank": "邮箱不能为空",
                                                                                              "required": "这个字段为必要字段"
                                                                                              })
    letter = serializers.CharField(required=True, max_length=30, help_text="厂商简称", label="厂商简称",
                                   error_messages={"blank": "厂商简称不能为空",
                                                   "required": "这个字段为必要字段"
                                                   })

    class Meta:
        model = Idc
        fields = ("id", "name", "address", "phone", "email", "letter")


class EnvSerializer(serializers.ModelSerializer):
    """
    环境序列化
    """
    name = serializers.CharField(max_length=50, help_text="环境名称", label="环境名称",
                                 error_messages={
                                     "blank": "环境名称不能为空",
                                     "required": "这个字段为必要字段"
                                 })

    class Meta:
        model = Env
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    项目序服务列化
    """

    def validate_pid(self, pid):
        if pid > 0:
            try:
                product_obj = Product.objects.get(pk=pid)
                if product_obj.pid != 0:
                    return serializers.ValidationError("上级业务线错误")
            except Product.DoesNotExist:
                return serializers.ValidationError("上级业务线不存在")
            return pid
        else:
            return 0

    def get_user_response(self, user_queryset):
        ret = []
        for dev in user_queryset:
            ret.append({
                "username": dev.username,
                "name": dev.name,
                "email": dev.email,
                "id": dev.id
            })
        return ret

    def get_idc_response(self, idc_queryset):
        ret = []
        for idc in idc_queryset:
            ret.append({
                "id": idc.id,
                "name": idc.name
            })
        return ret

    def create(self, validated_data):
        product_interfaces = validated_data.pop("product_interface")
        ops_interfaces = validated_data.pop("ops_interface")
        dev_interfaces = validated_data.pop("dev_interface")
        idcs = validated_data.pop("idc")
        product = Product.objects.create(**validated_data)
        for product_interface in product_interfaces:
            product.product_interface.add(product_interface)
        for ops_interface in ops_interfaces:
            product.ops_interface.add(ops_interface)
        for dev_interface in dev_interfaces:
            product.dev_interface.add(dev_interface)
        for idc in idcs:
            product.idc.add(idc)
        return product
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.product_interface = validated_data.get("product_interface", instance.product_interface)
    #     instance.ops_interface = validated_data.get("ops_interface", instance.ops_interface)
    #     instance.dev_interface = validated_data.get("dev_interface", instance.dev_interface)
    #     instance.idc = validated_data.get("idc", instance.idc)
    #     instance.pid = validated_data.get("pid", instance.pid)
    #     instance.save()
    #     return instance

    def to_representation(self, instance):
        dev_interface = self.get_user_response(instance.dev_interface.all())
        ops_interface = self.get_user_response(instance.ops_interface.all())
        product_interface = self.get_user_response(instance.product_interface.all())
        idc = self.get_idc_response(instance.idc.all())
        ret = super(ProductSerializer, self).to_representation(instance)
        ret["dev_interface"] = dev_interface
        ret["ops_interface"] = ops_interface
        ret["product_interface"] = product_interface
        ret["idc"] = idc
        return ret

    class Meta:
        model = Product
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    """
    服务器模型
    """
    LastCheck = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="检查时间")
    product = serializers.PrimaryKeyRelatedField(many=False, queryset=Product.objects.filter(pid__exact=0), label="项目",
                                                 help_text="项目")
    service = serializers.PrimaryKeyRelatedField(many=False, queryset=Product.objects.exclude(pid__exact=0), label="服务",
                                                 help_text="服务")

    def validate_idc(self, value):
        try:
            return Idc.objects.get(name=value)
        except Idc.DoesNotExist:
            return self.create_idc(value)

    def validate(self, attrs):
        return attrs

    def create_idc(self, idc_name):
        return Idc.objects.create(name=idc_name)

    def to_representation(self, instance):
        idc_obj = instance.idc
        product_obj = instance.product
        service_obj = instance.service
        ret = super(ServerSerializer, self).to_representation(instance)
        ret["idc"] = {
            "id": idc_obj.id,
            "name": idc_obj.name
        }
        if product_obj:
            ret["product"] = {
                "id": product_obj.id,
                "name": product_obj.name
            }
        else:
            ret["product"] = {}
        if service_obj:
            ret["service"] = {
                "id": service_obj.id,
                "name": service_obj.name
            }
        else:
            ret["service"] = {}
        if not instance.remark:
            ret["remark"] = ""
        return ret

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.product = validated_data.get("product", instance.product)
        instance.service = validated_data.get("service", instance.service)
        instance.idc = validated_data.get("idc", instance.idc)
        instance.remark = validated_data.get("remark", instance.remark)
        instance.save()
        return instance

    def to_internal_value(self, data):
        """
        反序列化第一步： 拿到的是提交过来的原始数据: QueryDict => request.GET,   request.POST
        """
        try:
            idc_obj = Idc.objects.get(name=data["idc"]["name"])
        except:
            return super(ServerSerializer, self).to_internal_value(data)
        else:
            ids = idc_obj.id
            data["idc"] = ids
            return super(ServerSerializer, self).to_internal_value(data)

    class Meta:
        model = Server
        # vm_status_dict = {0: "虚拟机", 1: "物理机", 2: "宿主机"}
        fields = '__all__'




# class ProductSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100, required=True)
#
#     def create(self, validated_data):
#         return Product.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.save()
#         return instance
#
#
# class AppSerializer(serializers.Serializer):
#     """
#     只读状态下使用
#     """
#     # product = serializers.SerializerMethodField()
#     # name = serializers.CharField(required=True)
#     #
#     # def get_product(self, obj):
#     #     print(obj.product)
#     #     return {
#     #         "id": obj.product.id,
#     #         "name": obj.product.name
#     #     }
#
#     product = serializers.PrimaryKeyRelatedField(many=False, queryset=Product.objects.all())
#     name = serializers.CharField(required=True, max_length=100)
#
#     def to_representation(self, instance):
#         product_obj = instance.product
#         ret = super(AppSerializer, self).to_representation(instance)
#         ret["product"] = {
#             "id": product_obj.id,
#             "name": product_obj.name
#         }
#         return ret
#
#     def to_internal_value(self, data):
#         '''
#         反序列化第一步： 拿到的是提交过来的原始数据: QueryDict => request.GET,   request.POST
#         '''
#
#         return super(AppSerializer, self).to_internal_value(data)
#
#     def create(self, validated_data):
#         # raise serializers.ValidationError("create error")
#         return Apps.objects.create(**validated_data)
#
#
# class IpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = IP
#         fields = "__all__"
#
#     # 字段级别验证
#     def validate_ipaddr(self, value):
#         print(value)
#         return value
#
#     # 表级别验证
#     def validate(self, attrs):
#         ip = attrs["ipaddr"]
#         try:
#             IP.objects.get(ipaddr__exact=ip)
#             raise serializers.ValidationError("IP已经存在")
#         except IP.DoesNotExist:
#             return attrs
#
#
# class ServerSerializer(serializers.Serializer):
#     hostname = serializers.CharField(required=True, max_length=50, label="主机名",help_text="主机名")
#     idc = serializers.PrimaryKeyRelatedField(many=False, queryset=Idc.objects.all(),label="idc", help_text="主机对应IDC")
#     app = serializers.PrimaryKeyRelatedField(many=False, queryset=Apps.objects.all(), label="应用", allow_null=True)
#     InstanceId = serializers.CharField(required=True, max_length=150, help_text="实例ID", label="实例ID")
#     ip = serializers.CharField(required=True, max_length=100, help_text="ip地址信息", label="ip")
#     cpu = serializers.CharField(required=True, max_length=10, help_text="cpu核数", label="cpu")
#     memory = serializers.CharField(required=True, max_length=30, help_text="内存", label="memory")
#     ExpirationTime = serializers.CharField(required=True, max_length=50, help_text="到期时间", label="到期时间")
#     os = serializers.CharField(required=True, max_length=100, help_text="系统", label="系统")
#     remark = serializers.CharField(required=True, max_length=300, help_text="服务器备注", label="备注")
#
#     def validate_idc(self, value):
#         try:
#             return Idc.objects.get(name=value)
#         except Idc.DoesNotExist:
#             return self.create_idc(value)
#
#     def validate(self, attrs):
#         return attrs
#
#     def create(self, validated_data):
#         return Server.objects.create(**validated_data)
#
#     def create_idc(self, idc_name):
#         return Idc.objects.create(name=idc_name)
#
#     def to_representation(self, instance):
#         idc_obj = instance.idc
#         InstanceId = instance.InstanceId
#         try:
#             ip = IP.objects.get(InstanceId=InstanceId)
#         except IP.DoesNotExist:
#             pass
#         else:
#             ret = super(ServerSerializer, self).to_representation(instance)
#             ret["idc"] = {
#                 "id": idc_obj.id,
#                 "name": idc_obj.name
#             }
#             ret["ip"] = ip.ipaddr
#
#
#             return ret
#
#     def to_internal_value(self, data):
#         '''
#         反序列化第一步： 拿到的是提交过来的原始数据: QueryDict => request.GET,   request.POST
#         '''
#         try:
#             idc_obj = Idc.objects.get(name=data["idc"]["name"])
#         except:
#             return super(ServerSerializer, self).to_internal_value(data)
#         else:
#             ids = idc_obj.id
#             data["idc"] = ids
#             return super(ServerSerializer, self).to_internal_value(data)
#
#     def update(self, instance, validated_data):
#         instance.cpu = validated_data.get("cpu", instance.cpu)
#         instance.memory = validated_data.get("memory", instance.memory)
#         instance.ExpirationTime = validated_data.get("ExpirationTime", instance.ExpirationTime)
#         instance.os = validated_data.get("os", instance.os)
#         instance.remark = validated_data.get("remark", instance.remark)
#         instance.save()
#         return instance
#
#
#
#
#
#     # def to_representation(self, instance):
#     #     idc_obj = instance.idc
#     #     app_obj = instance.app
#     #     print(app_obj)
#     #     ret = super(ServerSerializer, self).to_representation(instance)
#     #     ret["idc"] = {
#     #         "id": idc_obj.id,
#     #         "IdcName": idc_obj.IdcName
#     #     }
#
#         # return ret
#
#
# class DiskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Disk
#         fields = "__all__"
#
#     # def validate_server(self, value):
#     #     try:
#     #         Server.objects.get(pk=value)
#     #     except Server.DoesNotExist:
#     #         pass
#     #     return value
#     #
#     # def validate(self, attrs):
#     #     return attrs

