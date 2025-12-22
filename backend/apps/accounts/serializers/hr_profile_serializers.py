from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from ..models import HRProfile

User = get_user_model()


class HRUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_verified',
                  'is_active', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


class HRProfileSerializer(serializers.ModelSerializer):
    user = HRUserSerializer(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = HRProfile
        fields = [
            'id',
            'user',
            'user_email',
            'user_full_name',
            'bio',
            'phone',
            'company',
            'department',
            'linkedin',
            'contacts',
            'website',
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_by', 'created_at', 'updated_at']

    def validate_phone(self, value):
        if value and (len(value) < 9 or len(value) > 20):
            raise serializers.ValidationError("Телефон должен содержать от 9 до 20 символов")
        return value

    def validate_bio(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Биография не должна превышать 500 символов")
        return value


class HRSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    company_name = serializers.CharField(source='company', read_only=True)

    class Meta:
        model = HRProfile
        fields = [
            'id',
            'user_full_name',
            'user_email',
            'company_name',
            'department',
            'phone',
            'created_at',
        ]


class CreateHRSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)

    company = serializers.CharField(required=False, max_length=100, allow_blank=True)
    department = serializers.CharField(required=False, max_length=100, allow_blank=True)
    phone = serializers.CharField(required=False, max_length=20, allow_blank=True)
    bio = serializers.CharField(required=False, max_length=500, allow_blank=True)
    linkedin = serializers.URLField(required=False, allow_blank=True)
    contacts = serializers.CharField(required=False, max_length=200, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return email

    def validate_phone(self, value):
        if value and (len(value) < 9 or len(value) > 20):
            raise serializers.ValidationError("Телефон должен содержать от 9 до 20 символов")
        return value

    def create(self, validated_data):
        from ..models import HRProfile

        profile_fields = {
            'company': validated_data.pop('company', ''),
            'department': validated_data.pop('department', ''),
            'phone': validated_data.pop('phone', ''),
            'bio': validated_data.pop('bio', ''),
            'linkedin': validated_data.pop('linkedin', ''),
            'contacts': validated_data.pop('contacts', ''),
            'website': validated_data.pop('website', ''),
        }

        user = User.objects.create_hr_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        hr_profile = HRProfile.objects.create(
            user=user,
            created_by=self.context.get('request').user,
            **profile_fields
        )

        user.set_random_password_and_notify()

        return hr_profile


class UpdateHRProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = HRProfile
        fields = [
            'first_name',
            'last_name',
            'bio',
            'phone',
            'company',
            'department',
            'linkedin',
            'contacts',
            'website',
        ]

    def validate_phone(self, value):
        if value and (len(value) < 9 or len(value) > 20):
            raise serializers.ValidationError("Телефон должен содержать от 9 до 20 символов")
        return value

    def validate_bio(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Биография не должна превышать 500 символов")
        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class HRPasswordSetSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

