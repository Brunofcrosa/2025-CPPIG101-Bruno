from django import forms
from .models import Proprietario
import re

class ProprietarioModelForm(forms.ModelForm):
    class Meta:
        model = Proprietario
        fields = ['nome', 'endereco', 'telefone', 'email', 'foto']
        
        error_messages = {
            'nome': {'required': 'O nome do Proprietário é um campo obrigatório'},
            'endereco': {'required': 'O endereço do Proprietário é um campo obrigatório'},
            'telefone': {'required': 'O número do telefone é um campo obrigatório'},
            'email': {'required': 'O e-mail do Proprietário é um campo obrigatório',
                'invalid': 'Formato inválido para o e-mail. Exemplo de formato válido: fulano@dominio.com',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['placeholder'] = 'Fulano da imobiliária'
        self.fields['endereco'].widget.attrs['placeholder'] = 'Av. Roraima nº 1000 Cidade Universitária Bairro - Camobi, Santa Maria - RS, 97105-900'
        self.fields['telefone'].widget.attrs['placeholder'] = '(55) 99999-9999'
        self.fields['email'].widget.attrs['placeholder'] = 'proprietário@imobiliária.com'

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