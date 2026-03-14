from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Hospital, HospitalReview
from .serializers import HospitalSerializer, HospitalReviewSerializer
from authy.permissions import IsOwnerOrAdmin
from backend.cache_utils import CachedViewSetMixin
from django.conf import settings

# Create your views here.

class HospitalViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [AllowAny]
    cache_prefix = "hospitals"
    cache_ttl = settings.CACHE_TTL_LONG


    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        
        return super().get_permissions()

    
# class HospitalReviewViewSet(viewsets.ModelViewSet):
#     queryset = HospitalReview.objects.all()
#     serializer_class = HospitalReviewSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         qs = super().get_queryset()

#         if self.request.user.is_authenticated and self.action in ['update', 'partial_update', 'destroy'] and not self.request.user.is_superuser:
#             qs = qs.filter(user=self.request.user)

#         return qs
    

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             return [IsAdminUser(), IsAuthenticated()]
        

#         return super().get_permissions()



class HospitalReviewViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = HospitalReview.objects.all()
    serializer_class = HospitalReviewSerializer
    permission_classes = [AllowAny]
    cache_prefix = "hospital_reviews"
    cache_ttl = settings.CACHE_TTL_SHORT
    

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        
        return super().get_permissions()
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        self._invalidate_cache()
        # Also invalidate parent hospital cache since reviews are nested
        from backend.cache_utils import invalidate_prefix
        invalidate_prefix("hospitals")
