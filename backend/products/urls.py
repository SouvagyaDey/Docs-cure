# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductReviewSet, ProductViewSet, ProductStoreViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'productstore', ProductStoreViewSet, basename='productstore')
router.register(r'productreview', ProductReviewSet, basename='productreview')

urlpatterns = [
    path('', include(router.urls)),
]