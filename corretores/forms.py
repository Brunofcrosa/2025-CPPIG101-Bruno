from django import forms
from .models import Corretor
import re

class CorretorModelForm(forms.ModelForm):
    class Meta:
        model = Corretor
        fields = ['nome', 'endereco', 'telefone', 'email', 'foto']
        

        error_messages = {
            'nome': {'required': 'O nome do Corretor é um campo obrigatório.'},
            'endereco': {'required': 'O endereço do Corretor é um campo obrigatório.'},
            'telefone': {'required': 'O número do telefone é um campo obrigatório.'},
            'email': {
                'required': 'O e-mail do Corretor é um campo obrigatório.',
                'invalid': 'Formato inválido para o e-mail. Exemplo de formato válido: corretor@corretor.com.',
            }, 
            'foto': {'required': 'A foto do Corretor é um campo obrigatório.'}, 
        }
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            numeros = re.sub(r'\D', '', telefone)
            if not re.fullmatch(r'^\d{10,11}$', numeros):
                raise forms.ValidationError(
                    'O telefone deve conter exatamente 10 ou 11 dígitos numéricos (incluindo o DDD).'
                )
            
            if len(numeros) == 11:
                telefone_formatado = f'({numeros[0:2]}){numeros[2:7]}-{numeros[7:11]}'
            else: 
                telefone_formatado = f'({numeros[0:2]}){numeros[2:6]}-{numeros[6:10]}'
            
            return telefone_formatado
        return telefone