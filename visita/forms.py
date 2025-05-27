from django import forms
from .models import Visita

class VisitaModelForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['imovel', 'corretor', 'cliente', 'data', 'codigoVisita']
        
        error_messages = {
            'imovel': {'required': 'É um campo obrigatório'},
            'corretor': {'required': 'O corretor é um campo obrigatório'},
            'cliente': {'required': 'O cliente é um campo obrigatório'},
            'data': {'required': 'A data é um campo obrigatório'},
        }