from rest_framework.routers import DefaultRouter
from authentication.views import UserViewSet


api_router = DefaultRouter()
api_router.register('auth', UserViewSet)
