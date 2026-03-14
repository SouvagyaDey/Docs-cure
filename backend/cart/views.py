from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from orders.permissions import IsAdminOrOwner
from rest_framework.permissions import IsAuthenticated


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Cart.objects.all()
        return Cart.objects.filter(profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Get or create the current user's cart with all items."""
        cart, _ = Cart.objects.get_or_create(profile=request.user.profile)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear all items from the current user's cart."""
        try:
            cart = Cart.objects.get(profile=request.user.profile)
            cart.cart_items.all().delete()
            return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"message": "No cart found"}, status=status.HTTP_200_OK)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CartItem.objects.all()
        return CartItem.objects.filter(cart__profile=self.request.user.profile)

    def perform_create(self, serializer):
        # Auto-create cart if it doesn't exist
        cart, _ = Cart.objects.get_or_create(profile=self.request.user.profile)
        # Check if product already in cart - update quantity instead
        product = serializer.validated_data.get('product')
        existing = CartItem.objects.filter(cart=cart, product=product).first()
        if existing:
            existing.quantity += serializer.validated_data.get('quantity', 1)
            existing.save()
            return
        serializer.save(cart=cart)