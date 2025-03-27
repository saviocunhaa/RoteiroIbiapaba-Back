from django.contrib import admin
from .models import TouristSpot, TouristSpotImage

class TouristSpotImageInline(admin.TabularInline):
    model = TouristSpotImage
    extra = 3

class TouristSpotAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'categoria', 'data_criacao')
    list_filter = ('cidade', 'categoria')
    search_fields = ('nome', 'descricao', 'cidade')
    inlines = [TouristSpotImageInline]

admin.site.register(TouristSpot, TouristSpotAdmin)
admin.site.register(TouristSpotImage)
