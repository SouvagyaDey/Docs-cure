from rest_framework import viewsets
from products.models import ProductStore,Product,ProductReview
from products.serializers import ProductSerializer, ProductStoreSerializer,ProductReviewSerializer
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from backend.cache_utils import CachedViewSetMixin, invalidate_prefix
from django.conf import settings


class ProductViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    cache_prefix = "products"
    cache_ttl = settings.CACHE_TTL_MEDIUM

    def get_permissions(self):
        # Allow anyone to view products
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        # Only admins can create, update, delete
        return super().get_permissions()



class ProductStoreViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = ProductStore.objects.all()
    serializer_class = ProductStoreSerializer
    permission_classes = [IsAdminUser]
    cache_prefix = "productstores"
    cache_ttl = settings.CACHE_TTL_MEDIUM  


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        
        return super().get_permissions()


class ProductReviewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]
    cache_prefix = "product_reviews"
    cache_ttl = settings.CACHE_TTL_SHORT


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()


    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
        self._invalidate_cache()
        # Also invalidate parent product store cache since reviews are nested
        invalidate_prefix("productstores")