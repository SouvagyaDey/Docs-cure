from django.db import models
from django.utils import timezone
from django.db.models import Q
from authy.models import CustomUser
import uuid


def hospital_directory_path(instances , filename):
    return 'hospitals/hospital_image_{0}/{1}'.format(instances.name , filename)


class TypeCategories(models.TextChoices):
    GOVERNMENT = 'government', 'Government'
    PRIVATE = 'private', 'Private'
    CHARITY = 'charity', 'Charity'

class Hospital(models.Model):

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=hospital_directory_path, blank=True, null=True)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    category = models.CharField(max_length=100, choices=TypeCategories.choices, default=TypeCategories.PRIVATE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    bed_count = models.PositiveIntegerField(default=0)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    emergency_services = models.BooleanField(default=False)
    ambulance_service = models.BooleanField(default=False)
    blood_bank = models.BooleanField(default=False)
    pharmacy = models.BooleanField(default=False)
    cafeteria = models.BooleanField(default=False)
    parking_available = models.BooleanField(default=False)

    
    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"

        constraints = [
            models.CheckConstraint(
                name = 'bed_count_validation',
                check = Q(bed_count__gte=0),
                violation_error_message = 'Bed count must be greater than 0 !',
            ),

            models.CheckConstraint(
                name = 'established_year_validation',
                check = Q(established_year__gte=1800) & Q(established_year__lte=timezone.now().year),
                violation_error_message = 'Established year must be between 1800 and current year !',
            ),

            models.CheckConstraint(
                name = 'pincode_validation',
                check = Q(pincode__regex=r'^\d{6}$'),
                violation_error_message = 'Pincode must be a 6-digit number !',
            )
        ]

        ordering = ['name']
    


    def __str__(self):
        return self.name






class HospitalReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='rating_validation',
                check=Q(rating__gte=1) & Q(rating__lte=5),
                violation_error_message='Rating must be between 1 and 5!',
            )
        ]

        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.hospital.name}"