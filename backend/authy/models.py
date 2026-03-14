import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Q

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    class Meta:
        constraints = [
            models.CheckConstraint(
                name = 'email_validation',
                check = Q(email__endswith = '@gmail.com'),
                violation_error_message = 'enter valid email id !',
            )
        ]


    def __str__(self):
        return self.email
    


def profile_directory_path(instances , filename):
    return 'profiles/profile_image_{0}/{1}'.format(instances.id, filename)


class TypeRoleChoices(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        DOCTOR = 'doctor', 'Doctor'


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) # default related name is 'profile'
    role = models.CharField(max_length=10, choices=TypeRoleChoices.choices, default=TypeRoleChoices.PATIENT)
    profile_picture = models.ImageField(upload_to=profile_directory_path, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


   
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        
        return self.user.email.split('@')[0]
    
    

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        constraints = [
            models.CheckConstraint(
                name='phone_validation',
                check=Q(phone__regex=r'^\d{10}$'),
                violation_error_message='Phone number must be 10 digits long.',
            )
        ]


    def __str__(self):
        return f"{self.user.email} ({self.get_role_display()})"