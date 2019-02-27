# Create your tasks here
from __future__ import absolute_import, unicode_literals
import json, traceback, os, sys, django
from celery import shared_task
from scripts.ansible_api import ANSRunner
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opsweb.settings")
django.setup()

from cmdb.models import *


@shared_task(name="get_assets")
def get_asset(ip=None, group=None):
    """
    :param ip:
    :param group:
    :return:
    """
    host_dict = {}
    rbt = ANSRunner()
    if ip:
        ips = ip.replace(".", "_")
        rbt.run_model(ip, 'setup', '')
        host_info = rbt.get_model_result()['success'][ips]['ansible_facts']
    elif group:
        rbt.run_model(group, 'setup', '')
        host_info = rbt.get_model_result()['success'][group]['ansible_facts']
    host_dict['hostname'] = host_info['ansible_hostname']
    host_dict['cpu'] = host_info['ansible_processor_vcpus']
    host_dict['memory'] = host_info['ansible_memtotal_mb']
    os = host_info['ansible_distribution'] + ' ' + host_info['ansible_distribution_version']
    devices = host_info['ansible_devices']
    # devices_list = [{i: k['size']} for i, k in devices.items()]
    devices_dict = { k: v['size'] for k, v in devices.items() if k.startswith('v') }
    host_dict['os'] = os
    host_dict['devices'] = devices_dict
    server = Server.objects.filter(ip=ip)
    server.update(**host_dict)
    print(host_dict)