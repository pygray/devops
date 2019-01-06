# Create your tasks here
from __future__ import absolute_import, unicode_literals
import json, traceback
from celery import shared_task
from scripts.ansible_api import ANSRunner

# ansible 远程执行定时任务
@shared_task(name="crontab_task")
def run_cron_task():
    ansible_api = ANSRunner()
    playbook_path = '/etc/ansible/test.yml'
    res = ansible_api.run_playbook(playbook_path)
    return res

@shared_task(name="run_playbook")
def run_batch_task(playbook_path):
    try:
        rbt = ANSRunner()
        rbt.run_playbook(playbook_path)
        res = json.dumps(rbt.get_playbook_result(), indent=4)
        return res
    except:
        return traceback.print_exc()


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