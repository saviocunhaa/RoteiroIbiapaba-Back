import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from tourist_spots.models import TouristSpot

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos')
    ponto_turistico = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='favoritos')
    data_adicionado = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('usuario', 'ponto_turistico')
        
    def __str__(self):
        return f"{self.usuario.nome} - {self.ponto_turistico.nome}"
