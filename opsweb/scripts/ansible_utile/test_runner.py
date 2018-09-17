import sys
sys.path.append("/data/opsweb/scripts/ansible_utile")
import json
from runner import AdHocRunner, CommandRunner
from inventory import BaseInventory


def TestAdHocRunner(host, sctp_path_name):
        """
         以yml的形式 执行多个命令
        :return:
        """

        host_data = [
            {
                "hostname": "testserver",
                "ip": host,
                # "ip": "128.1.40.70",
                "port": 22,
                # "username": "root",
                # "password": "123456",
            },
        ]
        inventory = BaseInventory(host_data)
        runner = AdHocRunner(inventory)

        tasks = [
            # {"action": {"module": "cron","args": "name=\"sync time\" minute=\"*/3\" job=\"/usr/sbin/ntpdate time.nist.gov &> /dev/null\"" }, "name": "run_cmd"},
            {"action": {"module": "script", "args": sctp_path_name}, "name": "run_script"},
        ]
        ret = runner.run(tasks, "all")
        # print(ret.results_summary)
        print(json.dumps(ret.results_raw))
        return json.dumps(ret.results_raw)


def TestCommandRunner():
        """
        执行单个命令，返回结果
        :return:
        """

        host_data = [
            {
                "hostname": "testserver",
                "ip": "128.1.40.70",
                "port": 22,
                "username": "root",
                "password": "123456",
            },
        ]
        inventory = BaseInventory(host_data)
        runner = CommandRunner(inventory)
        res = runner.execute('/root/echo.sh', 'all', module='script')
        print(res.results_command)
        print(res.results_raw)
        # print(res.results_command['testserver']['stdout'])




# if __name__ == "__main__":
#     TestAdHocRunner()
#     TestCommandRunner()