import os
import django
import sys

# Setup Django
sys.path.append('/Users/souvagyadey/Desktop/Docscurev1/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from doctorappointment.models import Doctor
from authy.models import CustomUser, Profile
from hospitalmanagement.models import Hospital
import datetime

# Create sample doctors
doctors_data = [
    {
        'email': 'dr.smith@gmail.com',
        'specialization': 'cardiologist',
        'qualification': 'md',
        'experience_years': 15,
        'consultation_fee': 500,
        'languages_spoken': 'english',
        'first_name': 'John',
        'last_name': 'Smith',
        'bio': 'Experienced cardiologist with 15 years of practice',
    },
    {
        'email': 'dr.patel@gmail.com',
        'specialization': 'neurologist',
        'qualification': 'dm',
        'experience_years': 10,
        'consultation_fee': 600,
        'languages_spoken': 'english',
        'first_name': 'Priya',
        'last_name': 'Patel',
        'bio': 'Specialist in neurological disorders',
    },
    {
        'email': 'dr.kumar@gmail.com',
        'specialization': 'orthopedist', 
        'qualification': 'ms',
        'experience_years': 12,
        'consultation_fee': 450,
        'languages_spoken': 'hindi',
        'first_name': 'Rajesh',
        'last_name': 'Kumar',
        'bio': 'Expert in orthopedic surgery and sports injuries',
    },
    {
        'email': 'dr.lee@gmail.com',
        'specialization': 'pediatrician',
        'qualification': 'md',
        'experience_years': 8,
        'consultation_fee': 400,
        'languages_spoken': 'english',
        'first_name': 'Sarah',
        'last_name': 'Lee',
        'bio': 'Child care specialist',
    },
    {
        'email': 'dr.sharma@gmail.com',
        'specialization': 'dermatologist',
        'qualification': 'md',
        'experience_years': 7,
        'consultation_fee': 350,
        'languages_spoken': 'hindi',
        'first_name': 'Amit',
        'last_name': 'Sharma',
        'bio': 'Skin care and cosmetic dermatology expert',
    },
]

print("Adding doctors to database...")
count = 0

for doctor_info in doctors_data:
    try:
        # Check if profile already exists
        user = CustomUser.objects.filter(email=doctor_info['email']).first()
        
        if not user:
            # Create user
            user = CustomUser.objects.create_user(
                email=doctor_info['email'],
                password='doctor123'
            )
            print(f"Created user: {doctor_info['email']}")
        
        # Get or create profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'doctor',
                'first_name': doctor_info['first_name'],
                'last_name': doctor_info['last_name'],
                'bio': doctor_info['bio'],
            }
        )
        
        if not created:
            # Update profile if it exists
            profile.role = 'doctor'
            profile.first_name = doctor_info['first_name']
            profile.last_name = doctor_info['last_name']
            profile.bio = doctor_info['bio']
            profile.save()
        
        # Check if doctor already exists
        doctor, created = Doctor.objects.get_or_create(
            profile=profile,
            defaults={
                'specialization': doctor_info['specialization'],
                'qualification': doctor_info['qualification'],
                'experience_years': doctor_info['experience_years'],
                'consultation_fee': doctor_info['consultation_fee'],
                'languages_spoken': doctor_info['languages_spoken'],
            }
        )
        
        if created:
            count += 1
            print(f"✓ Added Dr. {doctor_info['first_name']} {doctor_info['last_name']} ({doctor_info['specialization']})")
        else:
            print(f"! Dr. {doctor_info['first_name']} {doctor_info['last_name']} already exists")
    
    except Exception as e:
        print(f"✗ Error adding {doctor_info['email']}: {str(e)}")

print(f"\n{'='*60}")
print(f"Summary: Added {count} new doctors")
print(f"Total doctors in database: {Doctor.objects.count()}")
print(f"{'='*60}")
