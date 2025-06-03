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

    def clean(self):
        cleaned_data = super().clean()
        imovel = cleaned_data.get('imovel') # Pega o imóvel da visita

        if imovel:
            # Verifica o status do imóvel antes de permitir o agendamento da visita
            if imovel.status_imovel() == 'Em Confirmação de Venda':
                raise forms.ValidationError(
                    "Não é possível agendar visitas para este imóvel, pois ele está em processo de confirmação de venda."
                )
            
        return cleaned_data