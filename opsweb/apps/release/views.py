from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .filter import deployFilter
from scripts.jenkins_api import JenkinsApi


from .serializers import DeploySerializer
from .models import Deploy
from time import sleep

User = get_user_model()



class DeployViewset(viewsets.ModelViewSet):
    """
    create:
    申请上线
    list:
    获取上线列表
    retrieve:
    获取上线信息
    update:
    代码更新信息
    delete:
    取消上线
    """
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Deploy.objects.all().order_by("-id")
    serializer_class = DeploySerializer
    filter_class = deployFilter
    filter_fields = ("keywords",)

    def get_queryset(self):
        status = self.request.GET.get('status',None)
        # print(status)
        applicant = self.request.user
        # print(applicant)
        role = applicant.groups.all().values('name')
        role_name = [ r['name'] for r in role]
        queryset = super(DeployViewset, self).get_queryset()

        # 判断传来的status值判断是申请列表还是历史列表
        if status and int(status) <= 2:
            queryset = queryset.filter(status__lte=2)
        elif status and int(status) > 2:
            queryset = queryset.filter(status__gte=2)
        else:
            pass

        # 判断登陆用户是否是管理员，是则显示所有工单，否则只显示自己的
        if "sa" not in role_name:
              queryset = queryset.filter(applicant=applicant)
        return queryset

    def partial_update(self, request, *args, **kwargs):
         pk = int(kwargs.get("pk"))
         data = request.data
         print(data)
         if data['status'] == 3:
             jenkins = JenkinsApi()
             number = jenkins.get_next_build_number(data['name'])
             jenkins.build_job(data['name'], parameters={'tag': data['version']})
             sleep(30)
             console_output = jenkins.get_build_console_output(data['name'], number)
             data['console_output'] = console_output
             print('2222')
         Deploy.objects.filter(pk=pk).update(**data)
         return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
         pk = int(kwargs.get("pk"))
         data = (request.data).dict()
         print(data)
         print(data['name'])
         print(data['version'])
         jenkins = JenkinsApi()
         number = jenkins.get_next_build_number(data['name'])
         jenkins.build_job(data['name'], parameters={'tag': data['version']})
         sleep(10)
         console_output = jenkins.get_build_console_output(data['name'], number)
         data['console_output'] = console_output
         print(data)
         Deploy.objects.filter(pk=pk).update(**data)
         return Response(status=status.HTTP_204_NO_CONTENT)
