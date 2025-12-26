from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vacancy
from .serializers import VacancySerializer
from rest_framework import permissions


class IsHROrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'hr'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.hr == request.user


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsHROrReadOnly]


    def perform_create(self, serializer):
        # Новые вакансии всегда создаются как черновик
        serializer.save(hr=self.request.user, status=Vacancy.Status.DRAFT)


    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        vacancy = self.get_object()

        if not vacancy.title or not vacancy.description:
            return Response(
                {'error': 'Заполните все обязательные поля'},
                status=400
            )

        vacancy.status = Vacancy.Status.PUBLISHED
        vacancy.save()
        return Response({'message': 'Вакансия опубликована'})


    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == 'admin':
            return queryset

        if user.role == 'hr':
            return queryset.filter(hr=user)

        return queryset.filter(status=Vacancy.Status.PUBLISHED)
