from rest_framework import serializers
from ..models import HRProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class HRSerializer(serializers.ModelSerializer):
    ...

class HRProfileSerializer(serializers.ModelSerializer):
    ...

