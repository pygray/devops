"""opsweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from cmdb.views import UploadFileViewSet

from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.schemas import get_schema_view


from rest_framework_jwt.views import obtain_jwt_token
from cmdb.router import cmdb_router
from account.router import account_router
from tasks.router import task_router
from release.router import deploy_router
from projects.router import project_router
from sqlmng.router import sql_router
from medias.router import media_router


schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

router = DefaultRouter()
router.registry.extend(account_router.registry)
router.registry.extend(cmdb_router.registry)
router.registry.extend(task_router.registry)
router.registry.extend(deploy_router.registry)
router.registry.extend(project_router.registry)
router.registry.extend(sql_router.registry)
router.registry.extend(media_router.registry)

urlpatterns = [
    url(r'^api/docs/', schema_view),
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-jwt/', obtain_jwt_token),
    url(r'^api-auth/', include("rest_framework.urls", namespace="rest_framework")),
    url(r'^docs/', include_docs_urls("transce")),
]
