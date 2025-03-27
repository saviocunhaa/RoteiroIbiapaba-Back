from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import SignupView, LogoutView, PasswordResetView, UserProfileView
from tourist_spots.views import TouristSpotViewSet
from favorites.views import FavoriteViewSet

# Swagger documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Roteiro Ibiapaba API",
      default_version='v1',
      description="API para o sistema Roteiro Ibiapaba - Pontos turísticos da Serra da Ibiapaba",
      terms_of_service="https://www.roteiro-ibiapaba.com/terms/",
      contact=openapi.Contact(email="contato@roteiro-ibiapaba.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'tourist-spots', TouristSpotViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    # Add a root URL pattern that redirects to swagger
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='api-root'),
    
    path('admin/', admin.site.urls),
    
    # Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Authentication endpoints
    path('api/auth/signup/', SignupView.as_view(), name='signup'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    
    # User profile
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    
    # API router
    path('api/', include(router.urls)),
]

# Serve static files in both development and production
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
