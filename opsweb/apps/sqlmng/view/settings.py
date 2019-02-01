from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from utils.baseviews import BaseView
from utils.basemixins import PromptMixins
from utils.baseviews import ReturnFormatMixin as res
from utils.permissions import IsSuperUser
from sqlmng.mixins import FixedDataMixins, CheckConn, HandleInceptionSettingsMixins
from sqlmng.data import variables, mail_actions, sql_settings
from sqlmng.serializers import *
from sqlmng.models import *

class SqlSettingsViewSet(FixedDataMixins, BaseView):
    '''
        设置SQL语句的属性（数量，拦截的字段）
    '''
    serializer_class = SqlSettingsSerializer
    permission_classes = [IsSuperUser]
    source_data = sql_settings

class StrategyViewSet(BaseView):
    '''
        设置审批策略
    '''
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
    permission_classes = [IsSuperUser]

class PersonalSettingsViewSet(PromptMixins, BaseView):
    '''
        审核工单的用户个性化设置
    '''
    serializer_class = PersonalSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

    def check_data(self, request_data):
        cluster = request_data.get('cluster')
        dbs = request_data.get('dbs')
        env = request_data.get('env')
        if not (cluster and dbs):
            raise ParseError(self.personal_variable_error)
        return cluster, dbs, env

    def create(self, request, *args, **kwargs):
        # save user
        request_data = request.data
        cluster, dbs, env = self.check_data(request_data)
        user = request.user
        data = {
            'leader': request_data.get('leader'),
            'admin_mail': request_data.get('admin_mail')
        }
        user_serializer = self.serializer_class(user, data=data)
        user_serializer.is_valid()
        user_serializer.save()
        alter_qs = user.dbconf_set.filter(cluster=cluster, env=env)
        for obj in alter_qs:
            user.dbconf_set.remove(obj)
        for db_id in dbs:
            user.dbconf_set.add(db_id)
        return Response(res.get_ret())

class InceptionVariablesViewSet(FixedDataMixins, HandleInceptionSettingsMixins, BaseView):
    '''
        Inception 变量
    '''
    serializer_class = InceptionVariablesSerializer
    permission_classes = [IsSuperUser]
    search_fields = ['name']
    source_data = variables

    def create(self, request, *args, **kwargs):
        self.set_variable(request)
        return Response(res.get_ret())

class MailActionsSettingsViewSet(FixedDataMixins, BaseView):
    '''
        发邮件对应的动作
    '''
    serializer_class = MailActionsSettingsSerializer
    permission_classes = [IsSuperUser]
    source_data = mail_actions

    def create(self, request, *args, **kwargs):
        model = self.serializer_class.Meta.model
        model.objects.all().update(value=False)
        model.objects.filter(name__in=request.data).update(value=True)
        return Response(res.get_ret())

class InceptionConnectionViewSet(BaseView):
    '''
        Inception连接信息
    '''
    queryset = InceptionConnection.objects.all()
    serializer_class = InceptionConnectionSerializer
    permission_classes = [IsSuperUser]

class InceptionBackupView(HandleInceptionSettingsMixins, viewsets.ViewSet):
    '''
        Inception备份信息
    '''
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        ret = res.get_ret()
        ret['data'] = self.get_inception_backup()
        return Response(ret)


class ConnectionCheckView(viewsets.ViewSet, CheckConn):
    '''
        检查连接(Inception连接/Inception备份库/目标库)
    '''
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print(request)
        res = self.check(request)
        return Response(res)