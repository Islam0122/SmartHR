from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'user_full_name',
            'user_email',
            'bio',
            'phone',
            'linkedin',
            'contacts',
            'website',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'user_full_name', 'user_email', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context.get('user')
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
