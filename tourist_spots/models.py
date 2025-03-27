import uuid
from django.db import models
from django.utils import timezone

class TouristSpot(models.Model):
    CATEGORY_CHOICES = (
        ('natural', 'Atração Natural'),
        ('historical', 'Ponto Histórico'),
        ('cultural', 'Atração Cultural'),
        ('adventure', 'Aventura'),
        ('religious', 'Religioso'),
        ('gastronomic', 'Gastronômico'),
        ('other', 'Outro'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    cidade = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    categoria = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    data_criacao = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.nome

class TouristSpotImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ponto_turistico = models.ForeignKey(TouristSpot, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='tourist_spots/')
    descricao = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"Imagem de {self.ponto_turistico.nome}"
