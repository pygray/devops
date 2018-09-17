from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()


def get_user_obj(uid):
    try:
        return User.objects.get(pk=uid)
    except User.DoesNotExist:
        return None


def get_permission_obj(pid):
    try:
        return Permission.objects.get(pk=pid)
    except Permission.DoesNotExist:
        return None