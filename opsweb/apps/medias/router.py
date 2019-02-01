from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from.views import SqlFileView

media_router = DefaultRouter()
media_router.register(r'media/download/sqlhandle/(?P<pk>\d+).(?P<sfx>\w+)', SqlFileView, base_name='download')

# urlpatterns = [
#     url(r'media/download/sqlhandle/(?P<pk>\d+).(?P<sfx>\w+)$', SqlFileView.as_view())
# ]