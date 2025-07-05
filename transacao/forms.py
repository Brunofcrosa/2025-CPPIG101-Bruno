import datetime
from django import forms
from .models import Transacao
from visita.models import Visita
from django.db.models import Q
from django.utils import timezone

class TransacaoModelForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['codigoImovel', 'codigoCorretor', 'codigoCliente', 'tipoTransacao', 'dataTransacao', 'statusTransacao', 'valorVenda']
        
        widgets = {
            'dataTransacao': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': datetime.date.today().isoformat()
                }
            ),
        }

        error_messages = {
          
        }
    
    def clean(self):
        cleaned_data = super().clean()
        imovel = cleaned_data.get('codigoImovel')
        tipo_transacao = cleaned_data.get('tipoTransacao')

        if imovel:
            existing_transactions = Transacao.objects.filter(
                codigoImovel=imovel
            ).exclude(
                pk=self.instance.pk if self.instance else None 
            ).filter(
                Q(statusTransacao='Pendente') | Q(statusTransacao='Concluída')
            )
            if existing_transactions.exists():
                raise forms.ValidationError("Este imóvel já possui uma transação em andamento ou concluída.")

            if imovel.status_imovel() == 'Em Confirmação de Venda' and tipo_transacao == 'Aluguel':
                raise forms.ValidationError(
                    "Este imóvel não pode ser alugado pois possui uma transação de venda pendente."
                )
            
            if tipo_transacao == 'Aluguel' and not imovel.disponivel_locacao:
                raise forms.ValidationError(
                    "Este imóvel não está marcado como disponível para locação."
                )

        return cleaned_data

    def save(self, commit=True):
        transacao = super().save(commit=False)
        
        imovel = transacao.codigoImovel
        tipo_transacao = transacao.tipoTransacao
        data_transacao = transacao.dataTransacao

        if tipo_transacao == 'Venda' and imovel and data_transacao:
            visitas_a_deletar = Visita.objects.filter(
                imovel=imovel,
                data__gte=data_transacao
            )
            visitas_a_deletar.delete()
        
        if commit:
            transacao.save()
        return transacao