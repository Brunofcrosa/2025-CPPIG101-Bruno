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
    
    def clean(self):
        cleaned_data = super().clean()
        imovel = cleaned_data.get('codigoImovel')
        tipo_transacao = cleaned_data.get('tipoTransacao')

        if imovel:
            if imovel.status_imovel() == 'Em Confirmação de Venda':
                if tipo_transacao == 'Aluguel':
                    raise forms.ValidationError(
                        "Este imóvel não pode ser alugado pois possui uma transação de venda pendente."
                    )
            
            if tipo_transacao == 'Aluguel' and not imovel.disponivel_locacao:
                raise forms.ValidationError(
                    "Este imóvel não está marcado como disponível para locação."
                )
        return cleaned_data