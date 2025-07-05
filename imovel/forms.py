from django import forms
from .models import Imovel
from transacao.models import Transacao
from decimal import Decimal
import re

class ImovelModelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = [
            'nome',
            'proprietario',
            'foto',
            'disponivel_locacao',
            'valorVenda',          
            'valorIPTU',           
            'valorCondominio',     
            'areaTotal',           
            'areaPrivativa',       
            'areaUtil',            
            'numQuartos',          
            'numBanheiros',        
            'vagasGaragem',        
            'tipoImovel',          
            'caracteristicas',     
            'comodidades',         
            'descricao',
            'zona_valorizacao',       
        ]
        
        error_messages = {
            'nome': {'required': 'Nome é obrigatório.'},
            'foto': {'required': 'Foto é obrigatória.'},
            'proprietario': {'required': 'Proprietário é obrigatório.'},
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        if self.instance.pk and self.instance.valorVenda is not None:
            self.initial['valorVenda'] = self.instance.get_valor_venda_br()

    def clean_valorVenda(self):
        valor_venda = self.cleaned_data.get('valorVenda')
        if valor_venda:
            
            valor_limpo = valor_venda.replace('.', '').replace(',', '.')
            try:
                
                return Decimal(valor_limpo)
            except Exception:
                raise forms.ValidationError("Formato inválido para o valor de venda. Use o formato 100.000,00.")
        return valor_venda

    def clean(self):
        cleaned_data = super().clean() 
        
        area_total = cleaned_data.get('areaTotal')
        area_privativa = cleaned_data.get('areaPrivativa')
        area_util = cleaned_data.get('areaUtil')

        valor_venda = cleaned_data.get('valorVenda')

        if area_privativa is not None and area_total is not None:
            if area_privativa > area_total:
                self.add_error(
                    'areaPrivativa', 
                    'A Área Privativa não pode ser maior que a Área Total.'
                )
        

        if area_util is not None and area_total is not None:
            if area_util > area_total:
                self.add_error(
                    'areaUtil', 
                    'A Área Útil não pode ser maior que a Área Total.'
                )

        if area_total is None and (area_privativa is not None or area_util is not None):
            self.add_error('areaTotal', 'A Área Total é obrigatória se a Área Privativa ou Útil forem preenchidas.')
            
        if self.instance.pk and 'valorVenda' in self.changed_data:
            imovel_original = Imovel.objects.get(pk=self.instance.pk)
        
            if imovel_original.pendencia_transacao():
                self.add_error(
                    'valorVenda',
                    'Não é possível alterar o valor de venda deste imóvel pois ele possui uma proposta de venda em andamento.'
                )

        return cleaned_data