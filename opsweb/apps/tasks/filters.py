import django_filters
from django.db.models import Q
from django_celery_beat.models import PeriodicTask
from django_celery_results.models import TaskResult


class TaskFilter(django_filters.FilterSet):
    keywords = django_filters.CharFilter(method="search_keyword")

    def search_keyword(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(task__icontains=value))

    class Meta:
        model = PeriodicTask
        fields = ["keywords"]


class TaskResultFilter(django_filters.FilterSet):
    keywords = django_filters.CharFilter(method="search_keyword")

    def search_keyword(self, queryset, name, value):
        return queryset.filter(Q(task_id__icontains=value) | Q(status__icontains=value))

    class Meta:
        model = TaskResult
        fields = ["keywords"]