from .views import CustomTokenObtainPairView, CustomRefreshTokenView, logout, is_authenticated, register, get_current_user, health_check
from django.urls import path


urlpatterns = [
    path('signup/', register, name='user-signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('logout/', logout, name='user-logout'),
    path('user/', get_current_user, name='get-current-user'),
    path("isauthenticated/", is_authenticated, name="is-authenticated"),
    path("token-refresh/", CustomRefreshTokenView.as_view(), name="token-refresh"),
    path("health/", health_check, name="health-check"),
]