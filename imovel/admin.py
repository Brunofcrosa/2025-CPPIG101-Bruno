# imovel/admin.py
from django.contrib import admin
from .models import Imovel

class ImovelAdmin(admin.ModelAdmin):
    list_display = ('codigoImovel', 'nome', 'endereco', 'disponivel_locacao', 'last_updated', 'is_outdated_display')
    list_filter = ('disponivel_locacao', 'tipoImovel', 'zona_valorizacao')
    search_fields = ('nome', 'codigoImovel', 'endereco')
    date_hierarchy = 'last_updated'
    readonly_fields = ('last_updated',)

    def is_outdated_display(self, obj):
        return obj.is_outdated()
    is_outdated_display.boolean = True
    is_outdated_display.short_description = 'Desatualizado'

admin.site.register(Imovel, ImovelAdmin)