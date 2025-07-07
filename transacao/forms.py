import datetime
from django import forms
from .models import Transacao
from visita.models import Visita
from django.db.models import Q
from decimal import Decimal

class TransacaoModelForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = [
            'codigoImovel', 'codigoCorretor', 'codigoCliente', 'tipoTransacao',
            'dataTransacao', 'statusTransacao', 'valorVenda',
            'valorAluguelMensal', 'dataInicioAluguel', 'dataFimAluguel', 'diaVencimentoAluguel'
        ]

        widgets = {
            'dataTransacao': forms.DateInput(attrs={'type': 'date'}),
            'dataInicioAluguel': forms.DateInput(attrs={'type': 'date'}),
            'dataFimAluguel': forms.DateInput(attrs={'type': 'date'}),
        }

        error_messages = {
            'codigoImovel': {'required': 'O imóvel é um campo obrigatório.'},
            'codigoCorretor': {'required': 'O corretor é um campo obrigatório.'},
            'codigoCliente': {'required': 'O cliente é um campo obrigatório.'},
            'tipoTransacao': {'required': 'O tipo de transação é um campo obrigatório.'},
            'dataTransacao': {'required': 'A data da transação é um campo obrigatório.'},
            'statusTransacao': {'required': 'O status da transação é um campo obrigatório.'},
            'valorVenda': {'required': 'O valor de venda é obrigatório para transações de Venda.'},
            'valorAluguelMensal': {'required': 'O valor do aluguel mensal é obrigatório para transações de Aluguel.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hoje = datetime.date.today().isoformat()
        self.fields['dataTransacao'].widget.attrs['min'] = hoje
        self.fields['dataInicioAluguel'].widget.attrs['min'] = hoje


        if self.instance.pk and self.instance.valorAluguelMensal is not None:
            self.initial['valorAluguelMensal'] = f"{self.instance.valorAluguelMensal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if self.instance.pk and self.instance.valorVenda is not None:
            self.initial['valorVenda'] = f"{self.instance.valorVenda:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


    def clean_valorVenda(self):
        valor_venda = self.cleaned_data.get('valorVenda')
        tipo_transacao = self.cleaned_data.get('tipoTransacao')

        if tipo_transacao == 'Venda' and valor_venda is None:
            raise forms.ValidationError("O valor de venda é obrigatório para transações de Venda.")

        if isinstance(valor_venda, str):
            valor_limpo = valor_venda.replace('.', '').replace(',', '.')
            try:
                return Decimal(valor_limpo)
            except Exception:
                raise forms.ValidationError("Formato inválido para o valor de venda. Use o formato 100.000,00.")
        return valor_venda

    def clean_valorAluguelMensal(self):
        valor_aluguel_mensal = self.cleaned_data.get('valorAluguelMensal')
        tipo_transacao = self.cleaned_data.get('tipoTransacao')

        if tipo_transacao == 'Aluguel' and valor_aluguel_mensal is None:
            raise forms.ValidationError("O valor do aluguel mensal é obrigatório para transações de Aluguel.")

        if isinstance(valor_aluguel_mensal, str):
            valor_limpo = valor_aluguel_mensal.replace('.', '').replace(',', '.')
            try:
                return Decimal(valor_limpo)
            except Exception:
                raise forms.ValidationError("Formato inválido para o valor do aluguel. Use o formato 1.000,00.")
        return valor_aluguel_mensal

    def clean_diaVencimentoAluguel(self):
        dia_vencimento = self.cleaned_data.get('diaVencimentoAluguel')
        tipo_transacao = self.cleaned_data.get('tipoTransacao')

        if tipo_transacao == 'Aluguel' and dia_vencimento is None:
            raise forms.ValidationError("O dia de vencimento do aluguel é obrigatório para transações de Aluguel.")
        
        if dia_vencimento is not None and not (1 <= dia_vencimento <= 31):
            raise forms.ValidationError("O dia de vencimento do aluguel deve ser entre 1 e 31.")
        return dia_vencimento

    def clean(self):
        cleaned_data = super().clean()
        imovel = cleaned_data.get('codigoImovel')
        tipo_transacao = cleaned_data.get('tipoTransacao')
        data_transacao = cleaned_data.get('dataTransacao')
        data_inicio_aluguel = cleaned_data.get('dataInicioAluguel')
        data_fim_aluguel = cleaned_data.get('dataFimAluguel')

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
        
        if tipo_transacao == 'Aluguel':
            if not data_inicio_aluguel:
                self.add_error('dataInicioAluguel', 'A data de início do aluguel é obrigatória para transações de Aluguel.')
            if not data_fim_aluguel:
                self.add_error('dataFimAluguel', 'A data de fim do aluguel é obrigatória para transações de Aluguel.')
            
            if data_inicio_aluguel and data_fim_aluguel and data_inicio_aluguel >= data_fim_aluguel:
                self.add_error('dataFimAluguel', 'A data de fim do aluguel deve ser posterior à data de início.')

            if data_inicio_aluguel and data_inicio_aluguel < datetime.date.today():
                self.add_error('dataInicioAluguel', 'A data de início do aluguel não pode ser no passado.')

        if tipo_transacao == 'Venda' and data_transacao and data_transacao < datetime.date.today():
            self.add_error('dataTransacao', 'A data da transação de venda não pode ser no passado.')


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