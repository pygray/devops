from rest_framework.routers import DefaultRouter
from .views import *

account_router = DefaultRouter()

account_router.register(r'userreg', UserRegViewset, base_name="userreg")
account_router.register(r'users', UsersViewSet, base_name="users")
account_router.register(r'userinfo', UserInfoViewset, base_name="userinfo")
account_router.register(r'groups', GroupsViewSet, base_name="groups")
account_router.register(r'usergroups', UserGroupsViewSet, base_name="usergroups")
account_router.register(r'groupmembers', GroupMembersViewSet, base_name="groupmembers")
account_router.register(r'permissions', PermissionsViewset, base_name="permissions")
account_router.register(r'grouppermissions', GroupPermissionsViewset, base_name="grouppermissions")