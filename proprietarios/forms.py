from django import forms
from .models import Proprietario

class ProprietarioModelForm(forms.ModelForm):
    class Meta:
        model = Proprietario
        fields = ['nome', 'endereco', 'telefone', 'email', 'foto']
        
        error_messages = {
            'nome': {'required': 'O nome do Proprietario é um campo obrigatório'},
            'endereco': {'required': 'O endereço do Proprietario é um campo obrigatório'},
            'telefone': {'required': 'O número do telefone é um campo obrigatório'},
            'email': {'required': 'O e-mail do Proprietario é um campo obrigatório',
                'invalid': 'Formato inválido para o e-mail. Exemplo de formato válido: fulano@dominio.com',
            }
        }