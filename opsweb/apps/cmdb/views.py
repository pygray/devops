from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets, response, status, mixins
from .filters import *
from .models import *

import json


# Create your views here.

class IdcViewSet(viewsets.ModelViewSet):
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
    filter_class = IdcFilter
    filter_fields = ("keywords",)

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_idc"):
            return super(IdcViewSet, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_idc"):
            return super(IdcViewSet, self).retrieve(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.change_idc"):
            return super(IdcViewSet, self).update(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        if request.user.has_perm("cmdb.delete_idc"):
            instance = self.get_object()

            if Server.objects.filter(idc_id__exact=instance.id).count() != 0:
                ret["status"] = 1
                ret["errmsg"] = "该IDC还有server记录，不能删除"
                return response.Response(ret, status=status.HTTP_200_OK)

            self.perform_destroy(instance)
            return response.Response(ret, status=status.HTTP_200_OK)
        else:
            ret["status"] = 1
            ret["errmsg"] = "此用户没有权限"
            return response.Response(json.dumps(ret))

    def create(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.add_idc"):
            return super(IdcViewSet, self).create(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))


class ProductViewSet(viewsets.ModelViewSet):
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

    filter_class = ProductFilter
    filter_fields = ("pid", )

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_product"):
            return super(ProductViewSet, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_product"):
            return super(ProductViewSet, self).retrieve(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.change_product"):
            return super(ProductViewSet, self).update(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def destroy(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.delete_product"):
            return super(ProductViewSet, self).destroy(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def create(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.add_product"):
            return super(ProductViewSet, self).create(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))


class ProductServiceViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin):
    """返回指定项目服务"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_product"):
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
        else:
            ret["status"] = 1
            ret["errmsg"] = "此用户没有权限"
            return response.Response(json.dumps(ret))


class IdcProductViewSet(mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    retrieve:
        返回指定厂商下项目信息
    """
    queryset = Idc.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_idc"):
            idc_obj = self.get_object()
            queryset = idc_obj.product_idc.filter(pid__exact=0)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            ret["status"] = 1
            ret["errmsg"] = "此用户没有权限"
            return response.Response(json.dumps(ret))


class ProductListViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    list:
        返回项目信息
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_product"):
            queryset = Product.objects.filter(pid__exact=0)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            ret["status"] = 1
            ret["errmsg"] = "此用户没有权限"
            return response.Response(json.dumps(ret))


class ServiceListViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    list:
        返回服务信息
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_product"):
            queryset = Product.objects.exclude(pid__exact=0)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            ret["status"] = 1
            ret["errmsg"] = "此用户没有权限"
            return response.Response(json.dumps(ret))


class ServerViewSet(viewsets.ModelViewSet):
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
    filter_class = ServerFilter
    filter_fields = ("keywords", "idc", "product", "service", )

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_server"):
            return super(ServerViewSet, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_server"):
            return super(ServerViewSet, self).retrieve(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def create(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.add_server"):
            return super(ServerViewSet, self).create(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.change_server"):
            return super(ServerViewSet, self).update(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def destroy(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.delete_server"):
            return super(ServerViewSet, self).destroy(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))


class ServiceTreeViewSet(viewsets.ViewSet,
                         mixins.ListModelMixin):
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("cmdb.view_product"):
            data = self.get_products()
            return response.Response(data)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

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









#
# class ProductViewset(viewsets.ModelViewSet):
#     """
#     retrieve:
#         返回指定product信息
#     list:
#         返回product列表
#     update:
#         更新product信息
#     destroy:
#         删除product记录
#     create:
#         创建product记录
#     partial_update:
#         更新部分字段
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class DiskViewset(viewsets.ModelViewSet):
#     """
#     create:
#         创建disk信息
#     update:
#         修改disk信息
#     destroy:
#         删除disk信息
#     retrieve:
#         返回指定disk信息
#     list:
#         返回disk列表
#     """
#     queryset = Disk.objects.all()
#     serializer_class = DiskSerializer
#
#
# class IpViewset(viewsets.ModelViewSet):
#     """
#     create:
#         创建IP信息
#     update:
#         修改IP信息
#     destroy:
#         删除IP信息
#     retrieve:
#         返回指定IP信息
#     list:
#         返回IP列表
#     """
#     queryset = IP.objects.all()
#     serializer_class = IpSerializer
#
#
# class ServerViewset(viewsets.ModelViewSet):
#     """
#     create:
#         创建server信息
#     update:
#         修改server信息
#     destroy:
#         删除server信息
#     retrieve:
#         返回指定server信息
#     list:
#         返回server列表
#     """
#     queryset = Server.objects.all()
#     serializer_class = ServerSerializer
#     filter_class = ServerFilter
#     filter_fields = ("keyword",)

