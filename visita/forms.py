from django import forms
from .models import Visita

class VisitaModelForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['nome', 'endereco', 'telefone', 'email', 'foto']
        
        error_messages = {
            'nome': {'required': 'O nome do cliente é um campo obrigatório'},
            'endereco': {'required': 'O endereço do cliente é um campo obrigatório'},
            'telefone': {'required': 'O número do telefone é um campo obrigatório'},
            'email': {'required': 'O e-mail do cliente é um campo obrigatório',
                'invalid': 'Formato inválido para o e-mail. Exemplo de formato válido: fulano@dominio.com',
                'unique': 'E-mail já cadastrado'
            }
        }