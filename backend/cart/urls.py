from rest_framework.routers import DefaultRouter
from django.urls import path, include   
from cart.views import CartItemViewSet, CartViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
