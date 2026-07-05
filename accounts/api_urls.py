from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import UserViewSet, LoginAPIView, LogoutAPIView, ProfileAPIView, DashboardStatsAPIView

router = DefaultRouter()
router.register('users', UserViewSet, basename='api-user')

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('auth/profile/', ProfileAPIView.as_view(), name='api-profile'),
    path('dashboard/stats/', DashboardStatsAPIView.as_view(), name='api-stats'),
    path('', include(router.urls)),
]
