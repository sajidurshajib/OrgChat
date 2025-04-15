from rest_framework import serializers
from .models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'detail']

class OrganizationSerializerWithId(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'detail']


class OrganizationDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=True,
        allow_empty=False
    )