from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import TouristSpot
from .serializers import TouristSpotSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import TouristSpot, TouristSpotImage
from .serializers import TouristSpotSerializer, TouristSpotImageSerializer

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
    
    def get_permissions(self):
        """
        Allow anyone to view tourist spots, but require authentication for other actions.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        """
        Upload an image for a tourist spot
        """
        tourist_spot = self.get_object()
        
        # Handle single image upload
        if 'imagem' in request.data:
            serializer = TouristSpotImageSerializer(data={
                'ponto_turistico': tourist_spot.id,
                'imagem': request.data['imagem'],
                'descricao': request.data.get('descricao', '')
            })
            
            if serializer.is_valid():
                serializer.save(ponto_turistico=tourist_spot)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle multiple image upload
        elif 'imagens' in request.data:
            images = request.FILES.getlist('imagens')
            data = []
            
            for image in images:
                image_serializer = TouristSpotImageSerializer(data={
                    'ponto_turistico': tourist_spot.id,
                    'imagem': image,
                    'descricao': request.data.get('descricao', '')
                })
                
                if image_serializer.is_valid():
                    image_serializer.save(ponto_turistico=tourist_spot)
                    data.append(image_serializer.data)
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'])
    def delete_image(self, request, pk=None):
        """
        Delete an image from a tourist spot
        """
        tourist_spot = self.get_object()
        image_id = request.query_params.get('image_id')
        
        if not image_id:
            return Response({'error': 'No image ID provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            image = TouristSpotImage.objects.get(id=image_id, ponto_turistico=tourist_spot)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TouristSpotImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
