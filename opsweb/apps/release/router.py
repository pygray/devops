from rest_framework.routers import DefaultRouter
from .views import DeployViewset, PreviewDeployListViewSet

deploy_router = DefaultRouter()
deploy_router.register(r'deploy', DeployViewset, base_name="deploy")
deploy_router.register(r'pre_deploy', PreviewDeployListViewSet, base_name="pre_deploy")