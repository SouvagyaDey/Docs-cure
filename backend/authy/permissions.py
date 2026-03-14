from rest_framework.permissions import BasePermission, SAFE_METHODS
from authy.models import TypeRoleChoices


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner
        return obj.user == request.user


class IsOwnerOrAdmin(BasePermission):
    """
    Only allow owners to edit their own reviews unless admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        # Allow admin users to edit any review
        return request.user.is_superuser or obj.user == request.user
    


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        profile = getattr(request.user, 'profile', None)

        if not profile:
            return False
        
        return profile.role == TypeRoleChoices.DOCTOR



class IsPatient(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        profile = getattr(request.user, 'profile', None)

        if not profile:
            return False

        return profile.role == TypeRoleChoices.PATIENT
        