from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Favorite
from .serializers import FavoriteSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar pontos turísticos favoritos do usuário.
    
    list:
    Retorna uma lista de todos os pontos turísticos favoritados pelo usuário autenticado.
    
    create:
    Adiciona um ponto turístico aos favoritos do usuário autenticado.
    
    retrieve:
    Retorna os detalhes de um favorito específico.
    
    destroy:
    Remove um ponto turístico dos favoritos do usuário autenticado.
    """
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Retorna apenas os favoritos do usuário autenticado.
        """
        return Favorite.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        """
        Associa o usuário autenticado ao favorito sendo criado.
        """
        serializer.save(usuario=self.request.user)
    
    @swagger_auto_schema(
        operation_description="Retorna uma lista de todos os pontos turísticos favoritados pelo usuário autenticado"
    )
    def list(self, request, *args, **kwargs):
        """
        Retorna uma lista de todos os pontos turísticos favoritados pelo usuário autenticado.
        """
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Adiciona um ponto turístico aos favoritos do usuário autenticado",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['ponto_turistico'],
            properties={
                'ponto_turistico': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID do ponto turístico')
            }
        ),
        responses={
            201: FavoriteSerializer,
            400: "Ponto turístico já favoritado ou inválido"
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Adiciona um ponto turístico aos favoritos do usuário autenticado.
        
        Verifica se o ponto turístico já está nos favoritos do usuário antes de adicionar.
        """
        # Check if the favorite already exists
        ponto_turistico_id = request.data.get('ponto_turistico')
        if Favorite.objects.filter(usuario=request.user, ponto_turistico_id=ponto_turistico_id).exists():
            return Response(
                {"detail": "Este ponto turístico já está em seus favoritos."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Retorna os detalhes de um favorito específico"
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os detalhes de um favorito específico.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Remove um ponto turístico dos favoritos do usuário autenticado"
    )
    def destroy(self, request, *args, **kwargs):
        """
        Remove um ponto turístico dos favoritos do usuário autenticado.
        """
        return super().destroy(request, *args, **kwargs)
