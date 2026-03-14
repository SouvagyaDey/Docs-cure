from rest_framework import serializers
from .models import Doctor, DoctorReview, Appointment
from authy.models import Profile
from hospitalmanagement.models import Hospital 
from authy.serializers import UserProfileSerializer
from hospitalmanagement.serializers import HospitalSerializer


class DoctorReviewSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DoctorReview
        fields = [
            'id',
            'doctor',
            'patient',
            'rating',
            'comment',
            'created_at'
        ]



class DoctorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    profile_id = serializers.PrimaryKeyRelatedField(
        source='profile', 
        queryset=Profile.objects.all(),
        write_only=True
    )
    profile = UserProfileSerializer(read_only=True)

    hospital_id = serializers.PrimaryKeyRelatedField(
        source='hospital', 
        queryset=Hospital.objects.all(),
        write_only=True
    )
    hospital = HospitalSerializer(read_only=True)

    doctor_reviews = DoctorReviewSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


    class Meta:
        model = Doctor
        fields = [
            'id',
            'profile_id',
            'profile',
            'hospital_id',
            'hospital',
            'specialization',
            'qualification',
            'experience_years',
            'consultation_fee',
            'start_available_days',
            'end_available_days',
            'start_available_time',
            'end_available_time',
            'languages_spoken',
            'doctor_reviews',
            'created_at',
            'updated_at'
        ]



class AppointmentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    patient = UserProfileSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        source='doctor', queryset=Doctor.objects.all(), write_only=True
    )
    doctor_updated = serializers.BooleanField(read_only=True)
    patient_status_updated = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'doctor',
            'doctor_id',
            'documents',
            'symptoms',
            'notes',
            'waiting_number',
            'doctor_updated',
            'patient_status_updated',
            'visit_fee',
            'bringing_documents',
            'appointment_date',
            'appointment_time',
            'status',
            'created_at',
            'updated_at'
        ]