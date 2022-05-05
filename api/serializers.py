from rest_framework import serializers
from core.models import Core


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Core
        fields = '__all__'