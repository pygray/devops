# Create your tasks here
from __future__ import absolute_import, unicode_literals
import json, traceback, os, django, sys
from celery import shared_task
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opsweb.settings")
django.setup()
from scripts.ansible_api import ANSRunner
from scripts.jenkins_api import JenkinsApi
from .models import Deploy
from time import sleep


@shared_task(name="preview_release")
def code_preview_release(pk, deploy):
    """
    后台执行上线任务（后台jenkins构建任务）
    :param deploy: Deploy实例(申请上线会往数据库里插一条记录，传过来的就是这条记录）
    :return:
    """
    jenkins = JenkinsApi()
    number = jenkins.get_next_build_number('test')
    jenkins.build_job('test', parameters={'tag': deploy['version']})
    sleep(15)
    console_output = jenkins.get_build_console_output('test', number)
    deploy['console_output'] = console_output
    Deploy.objects.filter(pk=pk).update(**deploy)
    return '[{}] Project release completed.......'.format('test')

