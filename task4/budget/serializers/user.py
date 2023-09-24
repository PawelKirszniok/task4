from django.contrib.auth.models import User
from rest_framework import serializers


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "is_active"]
