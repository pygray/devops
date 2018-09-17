# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from scripts.ansible_utile.test_runner import TestAdHocRunner


@shared_task
def run_script(host, scpt_path_name):
    res = TestAdHocRunner(host, scpt_path_name)
    print(res)
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