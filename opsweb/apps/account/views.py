from rest_framework import viewsets, mixins, response, status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from .filters import UserFilter, GroupFilter, PermissionFilter
from django.contrib.auth.models import Group, Permission
from .serializers import UserSerializer, UserRegSerializer, GroupSerializer, PermissionSerializer
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from menu.common import get_menu_tree

from account.common import get_user_obj, get_permission_obj
import json

User = get_user_model()


# Create your views here.


class UserRegViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    create:
    创建用户

    update:
    修改密码
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    获取用户信息
    list:
    获取用户列表
    update:
    更新用户信息
    delete:
    删除用户
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_fields = ("keywords", )
    # permission_classes = (IsAdminUser, )
    # extra_perms_map = {
    #     "GET": ["users.view_user"]
    # }

    # 权限细化控制
    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.view_user"):
            return super(UsersViewSet, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.change_userprofile"):
            return super(UsersViewSet, self).update(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.change_userprofile"):
            return super(UsersViewSet, self).retrieve(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def create(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.add_userprofile"):
            return super(UsersViewSet, self).create(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def destroy(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.delete_userprofile"):
            return super(UsersViewSet, self).destroy(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def get_queryset(self):
        queryset = super(UsersViewSet, self).get_queryset()
        queryset = queryset.order_by("id")
        queryset = queryset.exclude(is_superuser=True)
        return queryset


class GroupsViewSet(viewsets.ModelViewSet):
    """
    list:
    返回用户组（角色）列表
    destroy:
    删除角色
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    filter_fields = ("keywords",)
    # permission_classes = (IsAdminUser,)

    # 权限细化控制
    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.view_user"):
            return super(GroupsViewSet, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("auth.change_group"):
            return super(GroupsViewSet, self).update(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("auth.change_group"):
            return super(GroupsViewSet, self).retrieve(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def destroy(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("auth.delete_group"):
            return super(GroupsViewSet, self).destroy(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def create(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("auth.create_group"):
            return super(GroupsViewSet, self).create(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def get_queryset(self):
        queryset = super(GroupsViewSet, self).get_queryset()
        queryset = queryset.order_by("id")
        return queryset


class UserGroupsViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    retrieve:
    返回指定用户的所有角色
    update:
    修改当前用户的角色
    """
    queryset = User.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = (IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.view_user"):
            user_obj = self.get_object()
            queryset = user_obj.groups.all()

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("auth.change_user"):
            user_obj = self.get_object()
            gids = request.data.get("gid", [])
            user_obj.groups = Group.objects.filter(id__in=gids)
            return Response(status=status.HTTP_204_NO_CONTENT)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def get_queryset(self):
        queryset = super(UserGroupsViewSet, self).get_queryset()
        return queryset.order_by("id")


class GroupMembersViewSet(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
        角色成员管理
        retrieve:
        返回指定组的成员列表
        update:
        往指定组里添加成员
        destroy:
        从指定组里删除成员
        """
    queryset = Group.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.view_user"):
            instance = self.get_object()
            try:
                queryset = instance.user_set.all()
            except AttributeError:
                raise Http404
            username = request.GET.get("username", None)
            if username is not None:
                queryset = queryset.filter(Q(name__icontains=username) | Q(username__icontains=username))
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("auth.change_group"):
            ret = {"status": 0}
            group_obj = self.get_object()
            user_obj = get_user_obj(request.data.get(request.data.get("uid", 0)))
            if user_obj is None:
                ret["status"] = 1
                ret["errmsg"] = "用户错误"
            else:
                group_obj.user_set.add(user_obj)
            return Response(ret, status=status.HTTP_200_OK)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def destroy(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("auth.delete_group"):
            ret = {"status": 0}
            group_obj = self.get_object()
            user_obj = get_user_obj(request.data.get("uid", 0))
            if user_obj is None:
                ret["status"] = 1
                ret["errmsg"] = "用户错误"
            else:
                group_obj.user_set.remove(user_obj)
            return Response(ret, status=status.HTTP_200_OK)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))


class PermissionsViewset(viewsets.ReadOnlyModelViewSet):
    """
    权限列表 视图类
    list:
    返回permission列表
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_class = PermissionFilter
    filter_fields = ("keywords",)

    def list(self, request, *args, **kwargs):
        ret = {}
        # if request.user.has_perm("account.view_permission"):
        if request.user.has_perm("account.view_user)"):
            return super(PermissionsViewset, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def get_queryset(self):
        queryset = super(PermissionsViewset, self).get_queryset()
        queryset = queryset.order_by("content_type__id")
        return queryset


class GroupPermissionsViewset(viewsets.GenericViewSet,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin):
    """
    用户组权限
    retrieve:
    返回用户组的权限列表
    update:
    给指定用户组增加权限，参数pid: permission id
    destroy:
    删除指定组下的权限，参数pid: permission id
    """

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_class = PermissionFilter
    filter_fields = ("keywords",)

    def process_permission(self, group_permission_queryset, data):
        for record in data:
            try:
                group_permission_queryset.get(pk=record.get("id", None))
                record["status"] = True
            except:
                pass
        return data

    def get_group_permissions(self):
        groupobj = self.get_object()
        queryset = groupobj.permissions.all()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def get_modify_permissions(self):
        groupobj = self.get_object()
        group_permission_queryset = groupobj.permissions.all()
        queryset = Permission.objects.all()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self.process_permission(group_permission_queryset, serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(self.process_permission(group_permission_queryset, serializer.data))

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.view_user"):
            return super(GroupPermissionsViewset, self).list(request, *args, **kwargs)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def retrieve(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("account.view_user"):
            modify = request.GET.get("modify", None)
            if modify is not None:
                return self.get_modify_permissions()
            else:
                return self.get_group_permissions()
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def get_object(self):
        queryset = Group.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        ret = {}
        if request.user.has_perm("auth.change_permission"):
            ret = {"status": 0}
            groupobj = self.get_object()
            permission_obj = get_permission_obj(request.data.get("pid", ""))
            if permission_obj is None:
                ret["status"] = 1
                ret["errmsg"] = "permission 不存在"
            else:
                groupobj.permissions.add(permission_obj)
            return response.Response(ret, status=status.HTTP_200_OK)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        if request.user.has_perm("auth.delete_permission"):
            groupobj = self.get_object()
            permission_obj = get_permission_obj(request.data.get("pid", ""))
            if permission_obj is None:
                ret["status"] = 1
                ret["errmsg"] = "permission 不存在"
            else:
                groupobj.permissions.remove(permission_obj)
            return response.Response(ret, status=status.HTTP_200_OK)
        ret["status"] = 1
        ret["errmsg"] = "此用户没有权限"
        return response.Response(json.dumps(ret))


class DashboardViewset(viewsets.ViewSet):
    """
    非model 的权限使用
    list:
        dashboard api 数据
    """

    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        data = self.get_content_data()
        return response.Response(data)

    def get_content_data(self):
        return {
            "aa": 11,
            "bb": 22
        }


class UserInfoViewset(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    # extra_perms_map = {
    #     "GET": ["account.view_user"]
    # }

    # def list(self, request, *args, **kwargs):
    #     roles = list(request.user.get_all_permissions())
    #     roles_list = self.get_role_data(roles)
    #     if request.user.is_superuser:
    #         data = {
    #             "username": request.user.username,
    #             "name": request.user.name,
    #             "roles": ["admin"]
    #         }
    #     else:
    #         data = {
    #             "username": request.user.username,
    #             "name": request.user.name,
    #             "roles": roles_list
    #         }
    #     print(data)
    #     return response.Response(data)
    #
    # def get_role_data(self, roles):
    #     return [{k: v} for k, v in enumerate(roles)]

    def list(self, request, *args, **kwargs):
        data = {
            "username": self.request.user.username,
            "name": self.request.user.name,
            "menus": get_menu_tree(self.request.user.get_view_permissions()),
            "permissions": list(self.request.user.get_group_permissions())
        }
        return Response(data)
