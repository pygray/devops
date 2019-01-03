# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from scripts.ansible_test_api import AnsibleApi

# ansible 远程执行定时任务
@shared_task
def run_playbook():
    ansible_api = AnsibleApi()
    playbook_path = ['/etc/ansible/test.yml']
    res = ansible_api.runplayBook(playbook_path)
    return res


@shared_task
def add(x, y):
    print(x + y)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def sunlu(x, y):
    print(x + y)
    return x + y