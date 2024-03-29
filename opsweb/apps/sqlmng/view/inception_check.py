import re
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from utils.baseviews import BaseView
from utils.baseviews import ReturnFormatMixin as res
from utils.basemixins import PromptMixins
from workflow.serializers import WorkorderSerializer, StepSerializer
from sqlmng.mixins import ChangeSpecialCharacterMixins, ActionMixins
from sqlmng.serializers import *
from sqlmng.models import *

class InceptionCheckView(PromptMixins, ChangeSpecialCharacterMixins, ActionMixins, BaseView):
    '''
        SQL语法审核
    '''
    queryset = Inceptsql.objects.all()
    serializer_class = InceptionSerializer
    serializer_order = WorkorderSerializer
    serializer_step = StepSerializer

    def check_forbidden_words(self, sql_content):
        forbidden_instance = SqlSettings.objects.first()
        if forbidden_instance:
            forbidden_word_list = [fword for fword in self.convert(forbidden_instance.forbidden_words)]
            forbidden_words = [fword for fword in forbidden_word_list if re.search(re.compile(fword, re.I), sql_content)]
            if forbidden_words:
                raise ParseError({self.forbidden_words: self.reverse(forbidden_words)})

    def check_user_group(self, request):
        if request.data.get('env') == self.env_prd and not request.user.is_superuser:
            if not request.user.groups.exists():
                raise ParseError(self.not_exists_group)
            return request.user.groups.first().id

    def create_step(self, instance, users_id):
        if self.is_manual_review and instance.env == self.env_prd:
            users_id.append(None)
            for index, uid in enumerate(users_id):
                status = 1 if index == 0 else 0
                step_serializer = self.serializer_step(data={'work_order':instance.workorder_id, 'user':uid, 'status':status})
                step_serializer.is_valid(raise_exception=True)
                step_serializer.save()

    def get_strategy_is_manual_review(self, env):
        strategy_instance = Strategy.objects.first()
        if not strategy_instance:
            return False
        return strategy_instance.is_manual_review if env == self.env_prd else False

    def check_db(self, request_data):
        db = request_data.get('db')
        if not Dbconf.objects.filter(id=db):
            raise ParseError({self.not_exists_target_db})

    def check_count(self, request_data):
        sql_settings = SqlSettings.objects.first()
        if not sql_settings:
            raise ParseError({self.rules_warning})
        sql_content = request_data.get('sql_content')
        sql_list = sql_content.split(';')
        sql_list_count = len(sql_list) - 1
        sql_count_limit = sql_settings.sql_count_limit
        if sql_count_limit < sql_list_count:
            raise ParseError({self.sql_count_exceed.format(sql_list_count, sql_count_limit)})

    def create(self, request, *args, **kwargs):
        request_data = request.data
        self.check_count(request_data)
        self.check_db(request_data)
        request_data['group'] = self.check_user_group(request)
        request_data['treater'] = request_data.pop('treater_username')
        request_data['is_manual_review'] = self.get_strategy_is_manual_review(request_data.get('env'))
        sql_content = request_data.get('sql_content')
        select = re.search(self.type_select_tag, sql_content, re.IGNORECASE)
        self.check_forbidden_words(sql_content)
        if bool(select):
            handle_result_check = None
            request_data['type'] = self.type_select_tag
        else:
            handle_result_check = self.check_execute_sql(request_data.get('db'), sql_content, self.action_type_check)[-1]
        workorder_serializer = self.serializer_order(data={})
        workorder_serializer.is_valid()
        workorder_instance = workorder_serializer.save()
        request_data['handle_result_check'] = handle_result_check
        request_data['workorder'] = workorder_instance.id
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        self.create_step(instance, request_data['users'])
        self.mail(instance, self.action_type_check)
        return Response(res.get_ret())