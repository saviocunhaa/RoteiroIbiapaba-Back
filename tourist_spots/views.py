from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import TouristSpot
from .serializers import TouristSpotSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada que permite acesso de leitura a qualquer usuário,
    mas restringe operações de escrita apenas a administradores.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class TouristSpotViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualização e edição de pontos turísticos.
    
    list:
    Retorna uma lista paginada de todos os pontos turísticos.
    
    create:
    Cria um novo ponto turístico (apenas administradores).
    
    retrieve:
    Retorna os detalhes de um ponto turístico específico.
    
    update:
    Atualiza um ponto turístico (apenas administradores).
    
    partial_update:
    Atualiza parcialmente um ponto turístico (apenas administradores).
    
    destroy:
    Remove um ponto turístico (apenas administradores).
    """
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cidade', 'categoria']
    search_fields = ['nome', 'descricao', 'cidade']
    ordering_fields = ['nome', 'cidade', 'data_criacao']
    
    @swagger_auto_schema(
        operation_description="Retorna uma lista paginada de pontos turísticos",
        manual_parameters=[
            openapi.Parameter('cidade', openapi.IN_QUERY, description="Filtrar por cidade", type=openapi.TYPE_STRING),
            openapi.Parameter('categoria', openapi.IN_QUERY, description="Filtrar por categoria", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Buscar por nome, descrição ou cidade", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Ordenar por campo (ex: nome, -data_criacao)", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Retorna uma lista paginada de pontos turísticos.
        
        Permite filtrar por cidade e categoria, buscar por texto e ordenar por diferentes campos.
        """
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Cria um novo ponto turístico (apenas administradores)"
    )
    def create(self, request, *args, **kwargs):
        """
        Cria um novo ponto turístico.
        
        Apenas administradores podem criar pontos turísticos.
        """
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Retorna os detalhes de um ponto turístico específico"
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os detalhes de um ponto turístico específico.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Atualiza um ponto turístico (apenas administradores)"
    )
    def update(self, request, *args, **kwargs):
        """
        Atualiza um ponto turístico.
        
        Apenas administradores podem atualizar pontos turísticos.
        """
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Atualiza parcialmente um ponto turístico (apenas administradores)"
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente um ponto turístico.
        
        Apenas administradores podem atualizar pontos turísticos.
        """
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Remove um ponto turístico (apenas administradores)"
    )
    def destroy(self, request, *args, **kwargs):
        """
        Remove um ponto turístico.
        
        Apenas administradores podem remover pontos turísticos.
        """
        return super().destroy(request, *args, **kwargs)
