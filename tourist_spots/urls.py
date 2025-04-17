from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TouristSpotViewSet, GenerateItineraryView

router = DefaultRouter()
router.register(r'tourist-spots', TouristSpotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate-itinerary/', GenerateItineraryView.as_view(), name='generate-itinerary'),
]