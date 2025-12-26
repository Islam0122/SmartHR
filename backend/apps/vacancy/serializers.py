from rest_framework import serializers
from .models import Vacancy, Category, Specialization, Skill


class VacancySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True)
    specialization_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    skills_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'company_name',
            'description',
            'responsibilities',
            'requirements',
            'category_name',
            'specialization_name',
            'employment_type',
            'work_format',
            'experience_level',
            'location',
            'salary_from',
            'salary_to',
            'salary_currency',
            'salary_is_hidden',
            'skills_names',
            'ai_weight_config',
            'min_ai_score',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        hr = request.user if request else None

        category_name = validated_data.pop('category_name')
        specialization_name = validated_data.pop('specialization_name', None)
        skills_names = validated_data.pop('skills_names', [])

        category, _ = Category.objects.get_or_create(name=category_name.strip())

        specialization = None
        if specialization_name:
            specialization, _ = Specialization.objects.get_or_create(
                category=category,
                name=specialization_name.strip()
            )

        vacancy = Vacancy.objects.create(
            hr=hr,
            category=category,
            specialization=specialization,
            **validated_data
        )

        for skill_name in skills_names:
            skill, _ = Skill.objects.get_or_create(name=skill_name.strip())
            vacancy.skills.add(skill)

        return vacancy

    def validate(self, attrs):
        salary_from = attrs.get('salary_from')
        salary_to = attrs.get('salary_to')

        if salary_from and salary_to:
            if salary_from > salary_to:
                raise serializers.ValidationError({
                    'salary_from': 'Зарплата "от" не может быть больше "до"'
                })

        return attrs
