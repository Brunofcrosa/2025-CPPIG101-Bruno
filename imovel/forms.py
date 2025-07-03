from django import forms
from .models import Imovel
from transacao.models import Transacao

class ImovelModelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = [
            'nome',
            'proprietario',
            'endereco',
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
            'endereco': {'required': 'Endereço é obrigatório.'},
            'nome': {'required': 'Nome é obrigatório.'},
            'foto': {'required': 'Foto é obrigatória.'},
            'proprietario': {'required': 'Proprietário é obrigatório.'},
        }
        
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