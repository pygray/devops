from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectVersionsViewSet


project_router = DefaultRouter()
project_router.register(r'projects', ProjectViewSet, base_name="all projects")
project_router.register(r'tags', ProjectVersionsViewSet, base_name="tags")