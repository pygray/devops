from rest_framework.routers import DefaultRouter
from .views import *

account_router = DefaultRouter()

account_router.register(r'userreg', UserRegViewset, base_name="userreg")
account_router.register(r'users', UsersViewSet, base_name="users")
account_router.register(r'userinfo', UserInfoViewset, base_name="userinfo")
account_router.register(r'groups', GroupsViewSet, base_name="groups")
account_router.register(r'usergroup', UserGroupsViewSet, base_name="usergroup")
account_router.register(r'groupmembers', GroupMembersViewSet, base_name="groupmembers")
account_router.register(r'permission', PermissionViewSet, base_name="permission")
account_router.register(r'grouppower', GroupsPermViewSet, base_name="grouppower")