import django_filters
from django.db.models import Q
from release.models import Deploy

class deployFilter(django_filters.FilterSet):
    keywords = django_filters.CharFilter(method="search_keyword")
    status = Deploy.STATUS
    def search_keyword(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))

    class Meta:
        model = Deploy
        fields = ["keywords"]