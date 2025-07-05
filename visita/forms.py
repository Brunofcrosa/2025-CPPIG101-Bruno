from django import forms
import datetime
from datetime import timedelta
from .models import Visita


class VisitaModelForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['imovel', 'corretor', 'cliente', 'data', 'hora']

        widgets = {
            'data': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': datetime.date.today().isoformat()
                }
            ),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

        error_messages = {
            'imovel': {'required': 'É um campo obrigatório'},
            'corretor': {'required': 'O corretor é um campo obrigatório'},
            'cliente': {'required': 'O cliente é um campo obrigatório'},
            'data': {'required': 'A data é um campo obrigatório'},
            'hora': {'required': 'A hora é um campo obrigatória'},
        }

    def clean(self):
        cleaned_data = super().clean()
        imovel = cleaned_data.get('imovel')
        corretor = cleaned_data.get('corretor')
        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')

        if imovel:
            if imovel.status_imovel() == 'Em Confirmação de Venda':
                raise forms.ValidationError(
                    "Não é possível agendar visitas para este imóvel, pois ele está em processo de confirmação de venda."
                )

        if corretor and imovel and data and hora:
            proposed_dt = datetime.datetime.combine(data, hora)

            visitas_com_potencial_conflito = Visita.objects.filter(
                corretor=corretor,
                imovel=imovel,
                data=data
            )
            if self.instance and self.instance.pk:
                visitas_com_potencial_conflito = visitas_com_potencial_conflito.exclude(pk=self.instance.pk)

            for outra_visita in visitas_com_potencial_conflito:
                outra_visita_dt = datetime.datetime.combine(outra_visita.data, outra_visita.hora)
                diferenca_tempo = abs(proposed_dt - outra_visita_dt)

                if diferenca_tempo < timedelta(minutes=30):
                    self.add_error(
                        'hora',
                        f"O corretor já possui uma outra visita agendada em {outra_visita.data.strftime('%d/%m/%Y')} às {outra_visita.hora.strftime('%H:%M')}! (Mínimo exigido é de 30 minutos!)"
                    )
                    break
        return cleaned_data