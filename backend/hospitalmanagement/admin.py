from django.contrib import admin
from .models import Hospital, HospitalReview

# Register your models here.
admin.site.register(Hospital)
admin.site.register(HospitalReview)