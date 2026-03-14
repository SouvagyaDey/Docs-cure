from rest_framework import serializers
from .models import Hospital, HospitalReview



class HospitalReviewSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = HospitalReview
        fields = [
            'id', 
            'hospital', 
            'user', 
            'rating', 
            'comment', 
            'created_at'
        ]




class HospitalSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    hospital_reviews = HospitalReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Hospital
        fields = [
            'id',
            'image',
            'name',
            'state',
            'district',
            'address',
            'pincode',
            'category',
            'phone',
            'email',
            'website',
            'bed_count',
            'established_year',
            'emergency_services',
            'ambulance_service',
            'blood_bank',
            'pharmacy',
            'cafeteria',
            'parking_available',
            'hospital_reviews'
        ]