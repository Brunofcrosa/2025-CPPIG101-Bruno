from django import forms
from .models import Cliente

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'endereco', 'telefone', 'email', 'foto']
        
        error_messages = {
            'nome': {'required': 'O nome do cliente é um campo obrigatório'},
            'endereco': {'required': 'O endereço do cliente é um campo obrigatório'},
            'telefone': {'required': 'O número do telefone é um campo obrigatório'},
            'email': {'required': 'O e-mail do cliente é um campo obrigatório',
                'invalid': 'Formato inválido para o e-mail. Exemplo de formato válido: fulano@dominio.com',
            }
        }