from django.contrib import admin
from .models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ponto_turistico', 'data_adicionado')
    list_filter = ('data_adicionado',)
    search_fields = ('usuario__nome', 'ponto_turistico__nome')

admin.site.register(Favorite, FavoriteAdmin)
