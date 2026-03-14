from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from .permissions import IsAdminOrOwner, IsOwnerOfOrderOrAdmin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db import transaction


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrOwner]
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsOwnerOfOrderOrAdmin]
        elif self.action == "destroy":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        prev_status = order.status
        new_status = request.data.get("status", prev_status)

        # Handle status-only updates (e.g., cancel order)
        if set(request.data.keys()) <= {"status"}:
            if new_status == prev_status:
                return Response(
                    OrderSerializer(order).data,
                    status=status.HTTP_200_OK,
                )

            if new_status == "cancelled":
                if prev_status not in ["pending", "confirmed"]:
                    return Response(
                        {"error": "Only pending or confirmed orders can be cancelled."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                try:
                    with transaction.atomic():
                        # Restore stock
                        for item in order.order_items.all():
                            product = item.product
                            product.stock += item.quantity
                            product.save(update_fields=["stock"])
                        order.status = "cancelled"
                        order.save(update_fields=["status"])
                except Exception as e:
                    return Response(
                        {"error": str(e)},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                # Other status transitions (admin changing status)
                order.status = new_status
                order.save(update_fields=["status"])

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_200_OK,
            )

        # For full updates that include order_items, use the serializer
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__profile=user.profile)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action == "create":
            self.permission_classes = [IsOwnerOfOrderOrAdmin]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()