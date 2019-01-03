# -*- coding:utf-8 -*-
import json
import shutil
from ansible.plugins.callback import CallbackBase
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
import ansible.constants as C
from collections import namedtuple

class ModelResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result):
        self.host_failed[result._host.get_name()] = result

class AnsibleApi(object):
    def __init__(self):
        self.Options = namedtuple('Options',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass',
                      'module_path',
                      'forks',
                      'become',
                      'become_method',
                      'become_user',
                      'check',
                      'listhosts',
                      'listtasks',
                      'listtags',
                      'syntax',
                      'sudo_user',
                      'sudo',
                      'diff'])
        self.options = self.Options(connection='smart',
                  remote_user=None,
                  ack_pass=None,
                  sudo_user=None,
                  forks=5,
                  sudo=None,
                  ask_sudo_pass=False,
                  verbosity=5,
                  module_path=None,
                  become=None,
                  become_method=None,
                  become_user=None,
                  check=False,
                  diff=False,
                  listhosts=None,
                  listtasks=None,
                  listtags=None,
                  syntax=None)
        # 实例化解析yml
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources='/etc/ansible/hosts')
        # 实例化变量管理
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.callback = ModelResultsCollector()
        self.passwords = dict()

    def runadHoc(self, host_list, task_list):
        play_source = dict(
            # hosts为执行的主机或者群组
            name="Ansible Play ad-hoc",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in self.callback.host_failed.items():
            result_raw['failed'][host] = result._result

        print(json.dumps(result_raw, indent=4))
        return json.dumps(result_raw, indent=4)

    def runplayBook(self, playbook_path):
        self.variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes'}
        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.options, passwords=self.passwords)
        result = playbook.run()
        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in self.callback.host_failed.items():
            result_raw['failed'][host] = result._result

        print(json.dumps(result_raw, indent=4))

        return json.dumps(result_raw, indent=4)


# if __name__ == "__main__":
#     ansible_api = AnsibleApi()
#     host_list = ['test']
#     # tasks_list=[
#     #
#     #     dict(action=dict(module='ping', args='')),
#     #     # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
#     # ]
#     # ansible_api.runadHoc(host_list, tasks_list)
#     ansible_api.runplayBook(['/etc/ansible/test.yml'])
