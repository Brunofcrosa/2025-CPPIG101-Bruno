from django import forms
from .models import Imovel

class ImovelModelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = ['nome', 'proprietario', 'codigoImovel', 'endereco', 'foto',]
        
        error_messages = {
            'codigoImovel': {'required': 'Código do Imóvel é obrigatório.', 'unique': 'Este código já está cadastrado.',},
            'endereco': {'required': 'Endereço é obrigatório.'},
            'nome': {'required': 'Nome é obrigatório.'},
            'foto': {'required': 'Foto é obrigatória.'},
            'proprietario': {'required': 'Proprietário é obrigatório.'},
            }
        
