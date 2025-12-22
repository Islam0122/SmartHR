from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from ..models import StudentProfile
from ..serializers import (
    StudentProfileSerializer,
    StudentProfileDetailSerializer,
)


class StudentProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return StudentProfileDetailSerializer
        return StudentProfileSerializer

    def get_queryset(self):
        return StudentProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(StudentProfile, user=self.request.user)

    @extend_schema(
        description="Получить профиль текущего студента"
    )
    def list(self, request, *args, **kwargs):
        try:
            profile = StudentProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response({
                'error': 'Профиль студента не найден'
            }, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Обновить профиль студента"
    )
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Частично обновить профиль студента"
    )
    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)