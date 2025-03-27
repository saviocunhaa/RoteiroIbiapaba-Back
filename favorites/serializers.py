from rest_framework import serializers
from .models import Favorite
from tourist_spots.serializers import TouristSpotSerializer

class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer para gerenciamento de pontos turísticos favoritos.
    """
    ponto_turistico_detail = TouristSpotSerializer(source='ponto_turistico', read_only=True)
    
    class Meta:
        model = Favorite
        fields = ('id', 'usuario', 'ponto_turistico', 'ponto_turistico_detail', 'data_adicionado')
        read_only_fields = ('id', 'usuario', 'data_adicionado')
        extra_kwargs = {
            'ponto_turistico': {'help_text': 'ID do ponto turístico a ser favoritado'},
        }