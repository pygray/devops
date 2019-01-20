from django.views.generic import View
from rest_framework import viewsets, response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import  HttpResponse
from scripts.gitlab_api import  get_user_projects, get_project_versions
import  json


class ProjectViewSet(viewsets.ViewSet):
    '''
    list:
        获取用户所有项目
    retrieve:
        根据ID获取项目名称
    '''



    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        project_data = self.get_project_list()
        return response.Response(project_data)
    def get_project_list(self):
        my_projects = get_user_projects()
        json_list = []
        for project in my_projects:
            json_dict = {}
            json_dict['id'] = project.id
            json_dict['name'] = project.name
            json_dict['path_with_namespace'] = project.path_with_namespace
            json_dict['web_url'] = project.web_url
            json_dict['description'] = project.description
            json_list.append(json_dict)
        return json_list

    def get_one_project(self, pk):
        project_list = self.get_project_list()
        one_project_list = [ project for project in project_list if int(project['id']) == int(pk) ]
        return one_project_list


    def retrieve(self, request, pk=None):
        project_data = self.get_one_project(pk)
        return response.Response(project_data)





class ProjectVersionsViewSet(viewsets.ViewSet):
    """
    获取指定项目的所有版本
    """
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        tags = get_project_versions(int(pk))
        tag_list = [ {'name': tag.name, 'message': tag.message } for index, tag in enumerate(tags) ]
        return response.Response(tag_list)

