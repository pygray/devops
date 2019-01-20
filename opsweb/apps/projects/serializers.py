from rest_framework import serializers


class ProjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    # def to_representation(self, instance):
    #     ret = {}
    #     ret["role"] = 1
    #     return ret
