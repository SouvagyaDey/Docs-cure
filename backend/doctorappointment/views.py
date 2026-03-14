from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from authy.permissions import IsOwner, IsOwnerOrAdmin, IsDoctor, IsPatient
from .models import Doctor, DoctorReview, Appointment
from .serializers import DoctorSerializer, DoctorReviewSerializer, AppointmentSerializer
from rest_framework.response import Response
from rest_framework import status
from authy.models import TypeRoleChoices
from backend.cache_utils import CachedViewSetMixin, invalidate_prefix
from django.conf import settings

# Create your views here.

class DoctorViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]
    cache_prefix = "doctors"
    cache_ttl = settings.CACHE_TTL_LONG

    def get_permissions(self):
        if self.action in ['create']:
            return [IsDoctor()]
        
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        
        return super().get_permissions()

    

class DoctorReviewViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = DoctorReview.objects.all()
    serializer_class = DoctorReviewSerializer
    permission_classes = [AllowAny]
    cache_prefix = "doctor_reviews"
    cache_ttl = settings.CACHE_TTL_SHORT

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin(), IsAuthenticated()]
        
        return super().get_permissions()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        # Also invalidate parent doctor cache since reviews are nested
        invalidate_prefix("doctors")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        invalidate_prefix("doctors")

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        invalidate_prefix("doctors")
    
    
    

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]
        
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        
        if self.action in ['destroy']:
            return [IsAdminUser()]
        
        return super().get_permissions()
    

    def get_queryset(self):
        qs = super().get_queryset()

        user = self.request.user
        profile = user.profile

        view_type = self.request.query_params.get('view', None)

        if profile.role == TypeRoleChoices.DOCTOR:
            if view_type == 'my':
                # Doctor's own booked appointments (as a patient)
                return qs.filter(patient=profile.id)
            else:
                # Default: patient appointments assigned to this doctor
                return qs.filter(doctor=profile.doctor_profile.id)
        
        elif profile.role == TypeRoleChoices.PATIENT:
            return qs.filter(patient=profile.id)

        return qs
    

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.profile)


    def update(self, request, *args, **kwargs):
        appointment = self.get_object()
        user = request.user
        profile = user.profile

        role = getattr(profile, 'role', None)

        # Doctor update restriction
        if role == TypeRoleChoices.DOCTOR and appointment.doctor == profile.doctor_profile:
            if appointment.doctor_updated:
                return Response(
                    {"detail": "Doctor can only update once."},
                    status=status.HTTP_403_FORBIDDEN
                )
            

            appointment.doctor_updated = True

            appointment.save(update_fields=["doctor_updated"])

            response = super().update(request, *args, **kwargs)
            return response
        
        # Patient update restriction
        elif role == TypeRoleChoices.PATIENT and appointment.patient == profile:
            if not appointment.doctor_updated:
                return Response(
                    {"detail": "Patient can only update status after doctor update."},
                    status=status.HTTP_403_FORBIDDEN
                )

            if appointment.patient_status_updated:
                return Response(
                    {"detail": "Patient can only change status once."},
                    status=status.HTTP_403_FORBIDDEN
                )


            appointment.patient_status_updated = True

            appointment.save(update_fields=["patient_status_updated"])

            response = super().update(request, *args, **kwargs)
            return response


        # Admin with full update
        if user.is_superuser and user.is_staff:
            response = super().update(request, *args, **kwargs)
            return response
        

        return Response({"detail": f"Not allowed for {role}"}, status=status.HTTP_403_FORBIDDEN)