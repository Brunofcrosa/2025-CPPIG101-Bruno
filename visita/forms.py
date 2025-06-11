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
        imovel = cleaned_data.get('imovel') 
        corretor = cleaned_data.get('corretor') 
        data = cleaned_data.get('data')
        
        if imovel:
            if imovel.status_imovel() == 'Em Confirmação de Venda':
                raise forms.ValidationError(
                    "Não é possível agendar visitas para este imóvel, pois ele está em processo de confirmação de venda."
                )
            
        if data:
            if Visita.objects.filter(corretor=corretor, data=data).exists():
                raise forms.ValidationError(
                    "O corretor já tem uma visita agendada para esta data."
                )
            
        return cleaned_data