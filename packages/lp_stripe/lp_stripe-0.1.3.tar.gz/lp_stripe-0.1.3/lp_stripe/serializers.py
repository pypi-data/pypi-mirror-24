from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class SubscriptionCreateSerializer(serializers.Serializer):
    source = serializers.CharField()
    plan = serializers.CharField(required=True)
