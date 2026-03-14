from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet, HospitalReviewViewSet

router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet)
router.register(r'hospitalreviews', HospitalReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
]