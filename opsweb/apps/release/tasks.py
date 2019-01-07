# Create your tasks here
from __future__ import absolute_import, unicode_literals
import json, traceback
from celery import shared_task
from scripts.ansible_api import ANSRunner
from scripts.jenkins_api import JenkinsApi
from time import sleep

def code_release(deploy):
    """
    后台执行上线任务（后台jenkins构建任务）
    :param deploy: Deploy实例(申请上线会往数据库里插一条记录，传过来的就是这条记录）
    :return:
    """
    jenkins = JenkinsApi()
    number = jenkins.get_next_build_number(deploy.name)
    jenkins.build_job(deploy.name, parameters={'tag': deploy.version})
    sleep(30)
    console_output = jenkins.get_build_console_output(deploy.name, number)
    deploy.console_output = console_output
    deploy.save()
    return '[{}] Project release completed.......'.format(deploy.name)

