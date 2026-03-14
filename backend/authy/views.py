from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from django.conf import settings
from django.core.cache import cache

from .models import Profile
from .permissions import IsOwner
from .authentication import CookiesJWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from backend.cache_utils import CachedViewSetMixin, _make_user_key, invalidate_user_cache

# Create your views here.

# class AuthViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for Signup, Login, Logout using JWT
#     """
#     serializer_class = UserSignupSerializer
#     permission_classes = [AllowAny]
#     authentication_classes=[JWTAuthentication] 
    
#     # Signup
#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def create(self, request):
#         serializer = UserSignupSerializer(data=request.data)

#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)

#             return Response({
#                 "user": UserSerializer(user).data,
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#             }, status=status.HTTP_201_CREATED)
        

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Login
#     @action(detail=False, methods=["post"], permission_classes=[AllowAny])
#     def login(self, request):
#         email = request.data.get("email", "").strip()
#         password = request.data.get("password", "")

#         try:
#             user = authenticate(request, email=email, password=password)

#             if user is None:
#                 return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


#             # SimpleJWT token creation
#             refresh = RefreshToken.for_user(user)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         if not user.check_password(password):
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "user": UserSerializer(user).data,
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         })
    

#     # Logout (Blacklist token)
#     @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated], authentication_classes=[JWTAuthentication])
#     def logout(self, request):
#         refresh_token = request.data.get("refresh")

#         if not refresh_token:
#             return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()  # Blacklist the refresh token
#             return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
#         except TokenError:
#             return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            tokens = response.data or {}
            access_token = tokens.get("access")
            refresh_token = tokens.get("refresh")

            if not access_token or not refresh_token:
                return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

            # Use secure cookies in production; relax for local dev to allow HTTP
            secure = not settings.DEBUG
            samesite = "None" if secure else "Lax"

            res = Response({"success": True}, status=status.HTTP_200_OK)

            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=secure,
                samesite=samesite,
                path="/",
            )

            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=secure,
                samesite=samesite,
                path="/",
            )

            return res

        except Exception as e:
            return Response({"success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response({"detail": "No refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

            # Validate refresh token via serializer instead of mutating request.data
            serializer = self.get_serializer(data={"refresh": refresh_token})
            serializer.is_valid(raise_exception=True)
            access_token = serializer.validated_data.get("access")
            new_refresh_token = serializer.validated_data.get("refresh")

            secure = not settings.DEBUG
            samesite = "None" if secure else "Lax"

            res = Response({"refreshed": True}, status=status.HTTP_200_OK)
            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=secure,
                samesite=samesite,
                path="/",
            )

            # Update rotated refresh token cookie if rotation is enabled
            if new_refresh_token:
                res.set_cookie(
                    key="refresh_token",
                    value=new_refresh_token,
                    httponly=True,
                    secure=secure,
                    samesite=samesite,
                    path="/",
                )

            return res

        except Exception:
            return Response({"refreshed": False}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    try:
        secure = not settings.DEBUG
        samesite = "None" if secure else "Lax"

        res = Response({"success": True}, status=status.HTTP_200_OK)

        # Expire cookies by setting them to empty with max_age=0
        res.set_cookie(
            key="access_token",
            value="",
            httponly=True,
            secure=secure,
            samesite=samesite,
            path="/",
            max_age=0,
        )
        res.set_cookie(
            key="refresh_token",
            value="",
            httponly=True,
            secure=secure,
            samesite=samesite,
            path="/",
            max_age=0,
        )

        return res
    except Exception:
        return Response({"success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    return Response({
        "authenticated": True
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@authentication_classes([CookiesJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    try:
        cache_key = _make_user_key("current_user", request.user.id)
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        profile = Profile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        cache.set(cache_key, serializer.data, settings.CACHE_TTL_MEDIUM)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=404)

        


class UserProfileViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for User Profile
    """
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    cache_prefix = "profiles"
    cache_ttl = settings.CACHE_TTL_MEDIUM


    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]
        
        if self.action in ['update', 'partial_update']:
            return [IsOwner()]
        
        if self.action in ['destroy']:
            return [IsAdminUser()]
        
        return super().get_permissions()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        # Also invalidate per-user current_user cache
        user_id = serializer.instance.user_id
        invalidate_user_cache("current_user", user_id)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def health_check(request):
    return Response({"status": "healthy"}, status=status.HTTP_200_OK)