from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TouristSpotViewSet

router = DefaultRouter()
router.register(r'tourist-spots', TouristSpotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]