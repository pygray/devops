from rest_framework import viewsets
from rest_framework import filters

class ReturnFormatMixin(object):

    @classmethod
    def get_ret(cls):
        return {'status': 0, 'msg': '', 'data': {}}


class BaseView(viewsets.ModelViewSet):
    queryset = None
    serializer_class = None
    permission_classes = []
    # 搜索
    filter_backends = [filters.SearchFilter]
    search_fields = []