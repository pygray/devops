from django_celery_beat.models import PeriodicTask, PeriodicTask, IntervalSchedule, CrontabSchedule
from django_celery_results.models import TaskResult
from rest_framework import serializers
from .models import BatchTasks


class TaskSerializer(serializers.ModelSerializer):
    """
    任务序列化
    """

    data_changed = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="检查时间")
    last_run_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="上一次执行时间")
    # expires = serializers.DateTimeField(default="null", help_text="任务过期时间")

    def to_representation(self, instance):
        id = instance.id
        task_obj = PeriodicTask.objects.get(pk=id)
        crontab_obj = instance.crontab
        ret = super(TaskSerializer, self).to_representation(instance)
        try:
            ret["user"] = task_obj.task_profile.user
        except:
            ret["user"] = None
        if crontab_obj:
            ret["crontabs"] = "{} {} {} {} {}(m/h/d/dM/MY)".format(crontab_obj.minute, crontab_obj.hour,
                                                             crontab_obj.day_of_week, crontab_obj.day_of_month,
                                                             crontab_obj.month_of_year)
        return ret

    class Meta:
        model = PeriodicTask
        fields = "__all__"


class CrontabSerializer(serializers.ModelSerializer):
    """
    crontab表达式序列化
    """

    def to_representation(self, instance):
        ret = super(CrontabSerializer, self).to_representation(instance)
        ret["name"] = "{} {} {} {} {}(m/h/d/dM/MY)".format(instance.minute,
                                                           instance.hour,
                                                           instance.day_of_week,
                                                           instance.day_of_month,
                                                           instance.month_of_year)
        return ret

    class Meta:
        model = CrontabSchedule
        fields = "__all__"


class TaskResultSerializer(serializers.ModelSerializer):
    """
    task 结果序列化
    """

    date_done = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="完成时间")

    class Meta:
        model = TaskResult
        fields = "__all__"


class BatchTasksSerializer(serializers.ModelSerializer):
    """
    浠诲姟搴忓垪鍖栫被
    """

    class Meta:
        model = BatchTasks
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        instance = self.Meta.model.objects.create(**validated_data)
        instance.save()
        return instance