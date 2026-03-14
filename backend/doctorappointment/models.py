from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError
from authy.models import Profile
from hospitalmanagement.models import Hospital
import uuid
import datetime

# Create your models here.


def doctor_directory_path(instances , filename):
    return 'doctors/doctor_image_{0}/{1}'.format(instances.name , filename)


def pdf_upload_path(instance, filename):
    return 'patient_data/pdf_{0}/{1}'.format(instance.id, filename)


def get_default_date():
    return timezone.now().date()

def get_default_time():
    return timezone.now().time()


class SpecializationChoices(models.TextChoices):
    GENERAL = 'general', 'General'
    CARDIOLOGIST = 'cardiologist', 'Cardiologist'
    NEUROLOGIST = 'neurologist', 'Neurologist'
    ORTHOPEDIST = 'orthopedist', 'Orthopedist'
    PEDIATRICIAN = 'pediatrician', 'Pediatrician'
    GYNECOLOGIST = 'gynecologist', 'Gynecologist'
    DERMATOLOGIST = 'dermatologist', 'Dermatologist'
    PSYCHIATRIST = 'psychiatrist', 'Psychiatrist'
    ONCOLOGIST = 'oncologist', 'Oncologist'
    GASTROENTEROLOGIST = 'gastroenterologist', 'Gastroenterologist'
    PULMONOLOGIST = 'pulmonologist', 'Pulmonologist'
    ENDOCRINOLOGIST = 'endocrinologist', 'Endocrinologist'
    NEPHROLOGIST = 'nephrologist', 'Nephrologist'
    RHEUMATOLOGIST = 'rheumatologist', 'Rheumatologist'
    OPHTHALMOLOGIST = 'ophthalmologist', 'Ophthalmologist'
    ENT_SPECIALIST = 'ent specialist', 'Ent Specialist'
    ANESTHESIOLOGIST = 'anesthesiologist', 'Anesthesiologist'
    RADIOLOGIST = 'radiologist', 'Radiologist'
    PATHOLOGIST = 'pathologist', 'Pathologist'
    SURGEON = 'surgeon', 'Surgeon'
    SEXOLOGIST = 'sexologist', 'Sexologist'
    EMERGENCY = 'emergency', 'Emergency'


class QualificationChoices(models.TextChoices):
    MBBS = 'mbbs', 'Mbbs'
    MD = 'md', 'Md'
    MS = 'ms', 'Ms'
    DM = 'dm', 'Dm'
    MCH = 'mch', 'Mch'
    DIPLOMA = 'diploma', 'Diploma'
    FELLOWSHIP = 'fellowship', 'Fellowship'


class AvailableDaysChoices(models.TextChoices):
    MONDAY = 'monday', 'Monday'
    TUESDAY = 'tuesday', 'Tuesday'
    WEDNESDAY = 'wednesday', 'Wednesday'
    THURSDAY = 'thursday', 'Thursday'
    FRIDAY = 'friday', 'Friday'
    SATURDAY = 'saturday', 'Saturday'
    SUNDAY = 'sunday', 'Sunday'


class LanguageChoices(models.TextChoices):
    ASSAMESE = "assamese", "Assamese"
    BENGALI = "bengali", "Bengali"
    BODO = "bodo", "Bodo"
    DOGRI = "dogri", "Dogri"
    ENGLISH = "english", "English"
    GUJARATI = "gujarati", "Gujarati"
    HINDI = "hindi", "Hindi"
    KANNADA = "kannada", "Kannada"
    KASHMIRI = "kashmiri", "Kashmiri"
    KONKANI = "konkani", "Konkani"
    MAITHILI = "maithili", "Maithili"
    MALAYALAM = "malayalam", "Malayalam"
    MANIPURI = "manipuri", "Manipuri"
    MARATHI = "marathi", "Marathi"
    NEPALI = "nepali", "Nepali"
    ODIA = "odia", "Odia"
    PUNJABI = "punjabi", "Punjabi"
    SANSKRIT = "sanskrit", "Sanskrit"
    SANTALI = "santali", "Santali"
    SINDHI = "sindhi", "Sindhi"
    TAMIL = "tamil", "Tamil"
    TELUGU = "telugu", "Telugu"
    URDU = "urdu", "Urdu"


class Doctor(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name='doctor_profile')
    specialization = models.CharField(max_length=50, choices=SpecializationChoices.choices, default=SpecializationChoices.GENERAL)
    qualification = models.CharField(max_length=50, choices=QualificationChoices.choices,  default=QualificationChoices.MBBS)

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True, related_name='hospital_doctors')
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.PositiveIntegerField(default=300)

    # Availability
    start_available_days = models.CharField(
        max_length=10, 
        choices=AvailableDaysChoices.choices, 
        default=AvailableDaysChoices.MONDAY
    )

    end_available_days = models.CharField(
        max_length=10, 
        choices=AvailableDaysChoices.choices, 
        default=AvailableDaysChoices.FRIDAY
    )

    start_available_time = models.TimeField(default=datetime.time(9, 0))
    end_available_time = models.TimeField(default=datetime.time(17, 0))

    # Additional Information
    languages_spoken = models.CharField(max_length=200, choices=LanguageChoices.choices, default=LanguageChoices.ENGLISH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        name = self.profile.get_full_name() if self.profile else 'Unknown'
        return f"Dr. {name} - {self.get_specialization_display()}"
        


class DoctorReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_reviews")
    patient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=3)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Doctor Review'
        verbose_name_plural = 'Doctor Reviews'

        constraints = [
            models.CheckConstraint(
                name='rating_range',
                check=Q(rating__gte=1, rating__lte=5),
                violation_error_message='Rating must be between 1 and 5.',
            ),
            models.UniqueConstraint(
                fields=['doctor', 'patient'],
                name='unique_doctor_patient_review',
                violation_error_message='A patient can only review a doctor once.',
            )
        ]



class Appointment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending', 'pending'
        CONFIRMED = 'Confirmed', 'confirmed'
        RECONFIRMED = 'Reconfirmed', 'reconfirmed'
        COMPLETED = 'Completed', 'completed'
        CANCELLED = 'Cancelled', 'cancelled'
    
    # default
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # patient chooses
    patient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    documents = models.FileField(upload_to=pdf_upload_path, blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    #doctor chooses
    waiting_number = models.PositiveIntegerField(default=0)
    bringing_documents = models.TextField(blank=True, null=True)
    visit_fee = models.PositiveIntegerField(default=300)
    appointment_date = models.DateField(default=get_default_date)
    appointment_time = models.TimeField(default=get_default_time)

    # view logic
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    doctor_updated = models.BooleanField(default=False)
    patient_status_updated = models.BooleanField(default=False)

    # system generated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-appointment_date', '-appointment_time']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date', 'appointment_time'],
                name='unique_doctor_appointment'
            ),
        ]
    

    def clean(self):

        if self.appointment_date < timezone.localdate():
            raise ValidationError("Appointment date must be in the future.")
        
        if self.appointment_date == timezone.localdate() and self.appointment_time < timezone.localtime().time():
            raise ValidationError("Appointment time must be in the future.")


    def __str__(self):
        return f"{self.patient} - Dr. {self.doctor} on {self.appointment_date}"