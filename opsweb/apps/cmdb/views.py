from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, response, status, mixins
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FileUploadParser
from pyexcel_xlsx import get_data
from .models import *
from .tasks import get_asset
from utils.baseviews import BaseView


# Create your views here.

class IdcViewSet(BaseView):
    """
    retrieve:
        返回指定厂商信息
    list:
        返回厂商列表
    update:
        更新厂商信息
    destroy:
        删除厂商记录
    create:
        创建厂商记录
    partial_update:
        更新厂商部分字段
    """
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    search_fields = ['name', 'letter', 'email']

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        instance = self.get_object()
        if Server.objects.filter(idc_id__exact=instance.id).count() != 0:
            ret["status"] = 1
            ret["errmsg"] = "该IDC还有server记录，不能删除"
            return response.Response(ret, status=status.HTTP_200_OK)
        self.perform_destroy(instance)
        return response.Response(ret, status=status.HTTP_200_OK)


class ProductViewSet(BaseView):
    """
    retrieve:
        返回指定项目信息
    list:
        返回项目列表
    update:
        更新项目信息
    destroy:
        删除项目记录
    create:
        创建项目记录
    partial_update:
        更新项目部分字段
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    search_fields = ['pid']


class ProductServiceViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin):
    """返回指定项目服务"""

    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        product_obj = self.get_object()
        # pid = product_obj.pid
        ids = product_obj.id
        queryset = Product.objects.filter(pid__exact=ids)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class IdcProductViewSet(mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    retrieve:
        返回指定厂商下项目信息
    """
    queryset = Idc.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        idc_obj = self.get_object()
        queryset = idc_obj.product_idc.filter(pid__exact=0)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ServiceIPViewSet(viewsets.ViewSet):
    """
    list:
        返回服务和ip对应关系, 供 Ansible 发布调用
    """
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        data = {}
        service_obj = Product.objects.exclude(pid__exact=0)
        for s in service_obj:
            name = s.name
            server = Server.objects.filter(service=s)
            ip_list = [se.ip for se in server]
            data[name] = ip_list
        return Response(data)


class ServerViewSet(BaseView):
    """
    create:
        创建server信息
    update:
        修改server信息
    destroy:
        删除server信息
    retrieve:
        返回指定server信息
    list:
        返回server列表
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    search_fields = ["idc", "product", "service", "hostname", "ip"]

    def create(self, request, *args, **kwargs):
        data = request.data
        ip = data['ip']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 异步获取资产信息
        get_asset.delay(ip=ip)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ServerUpdateViewSet(viewsets.ViewSet,
                          mixins.UpdateModelMixin):
    """
    """
    queryset = Server.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = ServerUpdateSerializer

    def update(self, request, *args, **kwargs):
        pk = int(kwargs.get("pk"))
        data = request.data
        Server.objects.filter(pk=pk).update(**data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceTreeViewSet(viewsets.ViewSet,
                         mixins.ListModelMixin):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def list(self, request, *args, **kwargs):
            data = self.get_products()
            return response.Response(data)

    def get_products(self):
        ret = []
        for obj in self.queryset.filter(pid=0):
            node = self.get_node(obj)
            node["children"] = self.get_children(obj.id)
            ret.append(node)
        return ret

    def get_children(self, pid):
        ret = []
        for obj in self.queryset.filter(pid=pid):
            ret.append(self.get_node(obj))
        return ret

    def get_node(self, product_obj):
        node = {}
        node["id"] = product_obj.id
        node["label"] = product_obj.name
        node["pid"] = product_obj.pid
        return node


class UploadFileViewSet(viewsets.ViewSet):
    """
    文件上传
    """
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def create(self, request):
        file_obj = request.data["file"]
        data = get_data(file_obj)
        try:
            ips = data.get("工作表1")[1]
        except Exception:
            ips = data.get("sheet_1")[1]
        # 异步添加主机信息
        for ip in ips:
            server = Server.objects.filter(ip=ip)
            if not server:
                Server.objects.create(ip=ip)
            get_asset.delay(ip=ip)
        return Response(status=status.HTTP_204_NO_CONTENT)
