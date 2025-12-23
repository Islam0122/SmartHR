from rest_framework import serializers
from .models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    ai_enabled = serializers.SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'description',
            'requirements',
            'responsibilities',
            'company',
            'employment_type',
            'work_format',
            'experience_level',
            'location',
            'salary_from',
            'salary_to',
            'salary_currency',
            'skills',
            'min_ai_score',
            'status',
            'ai_enabled',
            'created_at',
        ]
        read_only_fields = ('status', 'created_at')

    def get_ai_enabled(self, obj):
        return bool(obj.skills and obj.ai_weight_config)
