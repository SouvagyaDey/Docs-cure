from rest_framework import permissions
from .models import Order

class IsAdminOrOwner(permissions.BasePermission):
    """
    Allow access only to authenticated users.
    Admins can access all objects.
    Owners can only access their own objects.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # Support both Order (profile) and Cart (profile) models
        if hasattr(obj, 'profile'):
            return obj.profile.user == request.user
        return False


class IsOwnerOfOrderOrAdmin(permissions.BasePermission):
    """
    Allow access only to the owner of the order (for POST) or to admins.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            order_id = request.data.get("order")
            if not order_id:
                return True  # Allow create without order_id (new order)
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return False
            return order.profile.user == request.user or request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'order'):
            return obj.order.profile.user == request.user
        if hasattr(obj, 'profile'):
            return obj.profile.user == request.user
        return False
