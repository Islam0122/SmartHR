from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import VacancyViewSet

router = DefaultRouter()
router.register(r'vacancies', VacancyViewSet, basename='vacancy')

urlpatterns = [
    path('', include(router.urls)),
]
