from rest_framework import serializers
from .models import TouristSpot, TouristSpotImage

class TouristSpotImageSerializer(serializers.ModelSerializer):
    """
    Serializer para imagens de pontos turísticos.
    """
    class Meta:
        model = TouristSpotImage
        fields = ('id', 'imagem', 'descricao')
        extra_kwargs = {
            'imagem': {'help_text': 'Arquivo de imagem do ponto turístico'},
            'descricao': {'help_text': 'Descrição opcional da imagem'},
        }

class TouristSpotSerializer(serializers.ModelSerializer):
    """
    Serializer para pontos turísticos.
    """
    imagens = TouristSpotImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = TouristSpot
        fields = ('id', 'nome', 'descricao', 'cidade', 'latitude', 'longitude', 'categoria', 'imagens', 'data_criacao')
        read_only_fields = ('id', 'data_criacao')
        extra_kwargs = {
            'nome': {'help_text': 'Nome do ponto turístico'},
            'descricao': {'help_text': 'Descrição detalhada do ponto turístico'},
            'cidade': {'help_text': 'Cidade onde o ponto turístico está localizado'},
            'latitude': {'help_text': 'Latitude da localização (formato decimal)'},
            'longitude': {'help_text': 'Longitude da localização (formato decimal)'},
            'categoria': {'help_text': 'Categoria do ponto turístico (natural, histórico, etc.)'},
            'imagens': {'help_text': 'Imagens relacionadas ao ponto turístico'},
        }  