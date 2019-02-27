from rest_framework import viewsets, mixins, response, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .filters import PermissionFilter
from django.contrib.auth.models import Group, Permission
from .serializers import UserSerializer, UserRegSerializer, Groupserializer, PermissionSerializer
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from utils.baseviews import BaseView
from utils.permissions import IsSuperUser

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


class UsersViewSet(BaseView):
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
    permission_classes = [IsSuperUser]
    search_fields = ['username', 'email']
    # permission_classes = (IsAdminUser, )
    # extra_perms_map = {
    #     "GET": ["users.view_user"]
    # }

    def get_queryset(self):
        queryset = super(UsersViewSet, self).get_queryset()
        queryset = queryset.order_by("id")
        queryset = queryset.exclude(is_superuser=True)
        return queryset


class GroupsViewSet(BaseView):
    """
    list:
    返回用户组（角色）列表
    destroy:
    删除角色
    """
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    permission_classes = [IsSuperUser]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super(GroupsViewSet, self).get_queryset()
        queryset = queryset.order_by("id")
        return queryset


class UserGroupsViewSet(mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    """
    update:
    修改指定用户的角色
    """
    permission_classes = [IsSuperUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 重写update方法，只针对用户和组进行单独的处理，类似的场景还有修改密码，更改状态等
    def update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        roles = request.data.get("role", [])
        user_obj.groups = roles
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupMembersViewSet(mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    destroy:
    从指定组里删除指定成员
    """
    permission_classes = [IsSuperUser]

    queryset = Group.objects.all()
    serializer_class = Groupserializer

    def destroy(self, request, *args, **kwargs):
        group_obj = self.get_object()
        uid = request.data.get('uid', 0)
        group_obj.user_set.remove(int(uid))
        return Response(status=status.HTTP_200_OK)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    权限列表 视图类
    list:
    返回permission列表
    """
    queryset = Permission.objects.all()
    permission_classes = [IsSuperUser]
    serializer_class = PermissionSerializer
    filter_class = PermissionFilter
    filter_fields = ("keywords",)

    def get_queryset(self):
        queryset = super(PermissionViewSet, self).get_queryset()
        queryset = queryset.order_by("content_type__id")
        return queryset


class GroupsPermViewSet(mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    """
    update:
    修改指定角色的权限
    """
    permission_classes = [IsSuperUser]
    queryset = Group.objects.all()
    serializer_class = Groupserializer

    def update(self, request, *args, **kwargs):
        group_obj = self.get_object()
        power = request.data.get("power", [])
        group_obj.permissions = power
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        if request.user.is_superuser:
            roles = ['admin']
        else:
            roles = list(self.request.user.get_group_permissions())
        data = {
            "username": self.request.user.username,
            "name": self.request.user.name,
            "roles": roles
        }
        return Response(data)
