from django import forms
from .models import Imovel

class ImovelModelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = [
            'nome',
            'proprietario',
            'codigoImovel',
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
        ]
        
        error_messages = {
            'codigoImovel': {'required': 'Código do Imóvel é obrigatório.', 'unique': 'Este código já está cadastrado.',},
            'endereco': {'required': 'Endereço é obrigatório.'},
            'nome': {'required': 'Nome é obrigatório.'},
            'foto': {'required': 'Foto é obrigatória.'},
            'proprietario': {'required': 'Proprietário é obrigatório.'},
        }
        
