from aliyunsdkcore.client import AcsClient
from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeDisksRequest, \
    DescribeNetworkInterfacesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
import json
import os, django, sys

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opsweb.settings")
django.setup()

from cmdb.models import *

accessKey_id = ""
accessKey_secret = ""
zone = "cn-hangzhou"


class AliyunApi:
    def __init__(self):
        self.client = AcsClient(accessKey_id, accessKey_secret, zone)

    def get_total_ip(self):
        """
        :return: ip总数量
        """
        request = DescribeNetworkInterfacesRequest.DescribeNetworkInterfacesRequest()
        request.set_accept_format('json')
        response = self.client.do_action(request)
        ip_info = json.loads(response.decode("utf-8"))
        total_num_count = ip_info["TotalCount"]
        return total_num_count

    def request_to_ip(self):
        """
        :return: ip信息
        """
        page_size = 50
        total_num_count = self.get_total_ip()

        page_num = total_num_count / page_size
        page_num = int(page_num) + 1
        ip_list = []
        for num in range(1, page_num + 1):
            request = DescribeNetworkInterfacesRequest.DescribeNetworkInterfacesRequest()
            request.set_PageNumber(num)
            request.set_PageSize(page_size)
            request.set_accept_format('json')
            response = self.client.do_action(request)
            response = json.loads(response)
            ip_info = response["NetworkInterfaceSets"]["NetworkInterfaceSet"]
            for ip in ip_info:
                ipaddrs = ip["PrivateIpSets"]["PrivateIpSet"]
                try:
                    mac = ip["MacAddress"]
                except KeyError:
                    continue
                try:
                    ipaddr = [ip["PrivateIpAddress"] for ip in ipaddrs]
                except:
                    continue
                else:
                    ips = {"InstanceId": ip["InstanceId"], "ipaddr": ipaddr, "mac": ip["MacAddress"],
                           "NetworkInterfaceId": ip["NetworkInterfaceId"]}
                ip_list.append(ips)
        return ip_list

    def get_total_disk(self):
        """
        :return: 磁盘总数量
        """
        request = DescribeDisksRequest.DescribeDisksRequest()
        request.set_accept_format('json')
        response = self.client.do_action(request)
        disk_info = json.loads(response.decode("utf-8"))
        total_num_count = disk_info["TotalCount"]
        return total_num_count

    def request_to_disk(self):
        """
        :return:  磁盘信息
        """
        page_size = 50
        total_num_count = self.get_total_disk()

        page_num = total_num_count / page_size
        page_num = int(page_num) + 1
        disk_list = []
        for num in range(1, page_num + 1):
            request = DescribeDisksRequest.DescribeDisksRequest()
            request.set_PageNumber(num)
            request.set_PageSize(page_size)
            request.set_accept_format('json')
            response = self.client.do_action(request)
            response = json.loads(response)
            disk_info = response["Disks"]["Disk"]
            for disk in disk_info:
                disks = {"InstanceId": disk["InstanceId"], "device": disk["Device"], "DiskSize": disk["Size"],
                         "disk": disk["DiskId"]}
                disk_list.append(disks)
        return disk_list

    def get_total_server(self):
        """
        :return: 服务器总数量
        """
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        response = self.client.do_action_with_exception(request)
        ecs_info = json.loads(response.decode("utf-8"))
        total_num_count = ecs_info["TotalCount"]
        return total_num_count

    def get_ecs_info(self):
        """

        :return: 服务器信息
        """
        page_size = 50
        total_num_count = self.get_total_server()

        page_num = total_num_count / page_size
        page_num = int(page_num) + 1
        ecs_list = []
        for num in range(1, page_num + 1):
            request = DescribeInstancesRequest.DescribeInstancesRequest()
            request.set_PageNumber(num)
            request.set_PageSize(page_size)
            response = self.client.do_action_with_exception(request)
            response = json.loads(response)
            esc_info = response["Instances"]["Instance"]
            for ecs in esc_info:
                ecs_list.append(ecs)
        return ecs_list

    def request_to_server(self):
        ecs_info_list = []
        ecs_info = self.get_ecs_info()
        for ecs in ecs_info:
            ip_info = ecs["VpcAttributes"]["PrivateIpAddress"]["IpAddress"]
            ip = ','.join(ip_info)
            ecs_dict = {
                "hostname": ecs["InstanceName"],
                "InstanceId": ecs["InstanceId"],
                "cpu": ecs["Cpu"],
                "ip": ip,
                "memory": ecs["Memory"],
                "os": ecs["OSName"],
            }
            ecs_info_list.append(ecs_dict)
        return ecs_info_list


if __name__ == "__main__":
    #disk_list = AliyunApi().request_to_disk()
    server_list = AliyunApi().request_to_server()
    for server_info in server_list:
        try:
            try:
                idc = Idc.objects.get(name="阿里云")
                server_info["idc"] = idc
            except:
                idc = Idc({"name": "阿里云"})
                idc.save()
            finally:
                server = Server(**server_info)
                server.save()
        except:
            server = Server.objects.filter(InstanceId=server_info["InstanceId"])
            server.update(**server_info)

    # for disk_info in disk_list:
    #     try:
    #         try:
    #             server = Server.objects.get(InstanceId=disk_info["InstanceId"])
    #             disk_info["server"] = server
    #         except:
    #             pass
    #         finally:
    #             disk = Disk(**disk_info)
    #             disk.save()
    #     except:
    #         disk = Disk.objects.filter(InstanceId=disk_info["InstanceId"])
    #         disk.update(**disk)
    # for ip_info in ip_list:
    #     try:
    #         ipaddr = ip_info["ipaddr"]
    #         if len(ipaddr) > 1:
    #             ipaddr = ",".join(ipaddr)
    #         elif len(ipaddr) == 1:
    #             ipaddr = ipaddr[0]
    #         ip_info["ipaddr"] = ipaddr
    #         server = Server.objects.get(InstanceId=ip_info["InstanceId"])
    #         ip_info["server"] = server
    #         ip = IP(**ip_info)
    #         ip.save()
    #     except:
    #         pass

    # AliyunApi().request_to_ip()
