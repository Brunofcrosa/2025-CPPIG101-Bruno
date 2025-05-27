from django import forms
from .models import Transacao

class TransacaoModelForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['codigoTransacao', 'codigoImovel', 'codigoCorretor', 'codigoCliente', 'tipoTransacao', 'dataTransacao', 'statusTransacao', 'valorVenda']
        
        error_messages = {
            'codigoTransacao' : {
                'required': 'O campo Código do Transação é obrigatório.',
                'unique': 'Já existe uma transação com este código.',
            }
        }