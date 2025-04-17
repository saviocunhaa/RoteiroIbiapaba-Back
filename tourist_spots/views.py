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
from rest_framework.views import APIView
import google.generativeai as genai
from django.conf import settings

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

# Add this new class at the end of the file
class GenerateItineraryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Gera um roteiro personalizado usando a API Gemini",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['dias'],
            properties={
                'cidade': openapi.Schema(type=openapi.TYPE_STRING, description='Cidade a visitar (ou "serra" para todas)'),
                'dias': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número de dias da viagem'),
                'interesses': openapi.Schema(type=openapi.TYPE_STRING, description='Interesses do usuário (opcional)'),
                'com_criancas': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Viagem com crianças (opcional)'),
                'hospedagem': openapi.Schema(type=openapi.TYPE_STRING, description='Local de hospedagem (opcional)'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Roteiro gerado com sucesso",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'roteiro': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: "Parâmetros inválidos",
            404: "Nenhum ponto turístico encontrado"
        }
    )
    def post(self, request):
        """
        Gera um roteiro personalizado usando a API Gemini.
        
        Recebe informações como cidade, número de dias e interesses do usuário,
        e retorna um roteiro detalhado com base nos pontos turísticos cadastrados.
        """
        cidade = request.data.get('cidade')
        dias = request.data.get('dias')
        interesses = request.data.get('interesses', '')
        com_criancas = request.data.get('com_criancas', False)
        hospedagem = request.data.get('hospedagem', '')

        if not dias:
            return Response({'error': 'Informe o número de dias da viagem.'}, status=status.HTTP_400_BAD_REQUEST)

        # If 'cidade' is 'serra', 'todas', or empty, fetch all spots
        if not cidade or cidade.strip().lower() in ['serra', 'todas', 'tudo', 'all']:
            spots = TouristSpot.objects.all()
            cidade_nome = "Serra da Ibiapaba"
        else:
            spots = TouristSpot.objects.filter(cidade__iexact=cidade)
            cidade_nome = cidade

        if not spots.exists():
            return Response({'error': 'Nenhum ponto turístico encontrado para esta região.'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare spot data for the prompt
        spots_data = []
        for spot in spots:
            # Get image URLs if available
            imagens = spot.imagens.all()
            imagem_info = f", Imagens disponíveis: {imagens.count()}" if imagens.exists() else ""
            
            spots_data.append(
                f"{spot.nome}: {spot.descricao} (Categoria: {spot.get_categoria_display()}, "
                f"Cidade: {spot.cidade}, Coordenadas: {spot.latitude},{spot.longitude}{imagem_info})"
            )
        
        spots_text = "\n".join(spots_data)

        # Build a comprehensive prompt for Gemini
        criancas_texto = "Sim, estou viajando com crianças. " if com_criancas else ""
        hospedagem_texto = f"Estarei hospedado em {hospedagem}. " if hospedagem else ""
        
        prompt = (
            f"Sou um turista e vou passar {dias} dias na região {cidade_nome}. "
            f"{criancas_texto}{hospedagem_texto}"
            f"Meus interesses são: {interesses if interesses else 'diversos'}. "
            f"Esses são os pontos turísticos cadastrados na região:\n\n{spots_text}\n\n"
            "Por favor, monte um roteiro diário detalhado e otimizado, sugerindo quais pontos visitar em cada dia, "
            "considerando a proximidade geográfica, variedade de experiências e aproveitamento do tempo. "
            "Inclua sugestões de horários para cada atração e dicas práticas. "
            "Organize o roteiro por dia (Dia 1, Dia 2, etc.) e seja objetivo. "
            "Responda em português do Brasil."
        )

        try:
            # Call Gemini API
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            if hasattr(response, 'text'):
                roteiro = response.text
            else:
                roteiro = response.candidates[0].content.parts[0].text
                
            return Response({'roteiro': roteiro})
        except Exception as e:
            return Response({'error': f'Erro ao gerar roteiro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
