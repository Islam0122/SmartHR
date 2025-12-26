from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vacancy
from .serializers import VacancySerializer


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(hr=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.request.query_params.get('category')
        specialization_name = self.request.query_params.get('specialization')
        status = self.request.query_params.get('status')

        if category_name:
            queryset = queryset.filter(category__name__icontains=category_name)
        if specialization_name:
            queryset = queryset.filter(specialization__name__icontains=specialization_name)
        if status:
            queryset = queryset.filter(status=status)

        return queryset
