from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .view.inception_check import InceptionCheckView
from .view.select_data import SelectDataView
from .view.target_db import DbViewSet
from .view.workorder_main import InceptionMainView
from .view.auth_rules import AuthRulesViewSet
from .view.suggestion import SuggestionViewSet
from .view.db_cluster import DbClusterViewSet
from .view.settings import \
    SqlSettingsViewSet, \
    StrategyViewSet, \
    PersonalSettingsViewSet, \
    InceptionVariablesViewSet, \
    InceptionConnectionViewSet, \
    MailActionsSettingsViewSet, \
    InceptionBackupView, \
    ConnectionCheckView


sql_router = DefaultRouter()
sql_router.register(r'dbconfs', DbViewSet, base_name='DbViewSet')
sql_router.register(r'inceptions', InceptionMainView, base_name='InceptionMainView')
sql_router.register(r'inceptioncheck', InceptionCheckView, base_name='InceptionCheckView')
sql_router.register(r'autoselects', SelectDataView, base_name='SelectDataView')
sql_router.register(r'sqlsettings', SqlSettingsViewSet, base_name='SqlSettingsViewSet')
sql_router.register(r'strategy', StrategyViewSet, base_name='StrategyViewSet')
sql_router.register(r'personalsettings', PersonalSettingsViewSet, base_name='PersonalSettingsViewSet')
sql_router.register(r'authrules', AuthRulesViewSet, base_name='AuthRulesViewSet')
sql_router.register(r'suggestion', SuggestionViewSet, base_name='SuggestionViewSet')
sql_router.register(r'dbcluster', DbClusterViewSet, base_name='DbClusterViewSet')
sql_router.register(r'mailactions', MailActionsSettingsViewSet, base_name='MailActionsSettingsViewSet')
sql_router.register(r'inception/variables', InceptionVariablesViewSet, base_name='InceptionVariablesViewSet')
sql_router.register(r'inception/connection', InceptionConnectionViewSet, base_name='InceptionConnectionViewSet')

urlpatterns = [
    url(r'^', include(sql_router.urls)),
    url(r'^inception/backup/$', InceptionBackupView.as_view()),
    url(r'^inception/conncheck/$', ConnectionCheckView.as_view())
]