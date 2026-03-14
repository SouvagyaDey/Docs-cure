from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, DoctorReviewViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'doctor_reviews', DoctorReviewViewSet)
router.register(r'appointments', AppointmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]