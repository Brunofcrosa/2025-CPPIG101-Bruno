from django import forms
from .models import Corretor

class CorretorModelForm(forms.ModelForm):
    class Meta:
        model = Corretor
        fields = ['nome', 'endereco', 'telefone', 'email', 'foto']
        
        error_messages = {
            'nome': {'required': 'O nome do Corretor é um campo obrigatório'},
            'endereco': {'required': 'O endereço do Corretor é um campo obrigatório'},
            'telefone': {'required': 'O número do telefone é um campo obrigatório'},
            'email': {'required': 'O e-mail do Corretor é um campo obrigatório',
                'invalid': 'Formato inválido para o e-mail. Exemplo de formato válido: fulano@dominio.com',
            }
        }