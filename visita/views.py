from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Visita
from .forms import VisitaModelForm

class VisitaView(ListView):
    model = Visita
    template_name = 'visitas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(VisitaView, self).get_queryset()
        
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum agendamento encontrado')

class VisitaAddView(SuccessMessageMixin, CreateView):
    model = Visita
    form_class = VisitaModelForm
    template_name = 'visita_form.html'
    success_url = reverse_lazy('visita')
    success_message = 'Agendamento cadastrado com sucesso!'

class VisitaUpdateView(SuccessMessageMixin, UpdateView):
    model = Visita
    form_class = VisitaModelForm
    template_name = 'visita_form.html'
    success_url = reverse_lazy('visita')
    success_message = 'Agendamento alterado com sucesso!'

class VisitaDeleteView(SuccessMessageMixin, DeleteView):
    model = Visita
    template_name = 'visita_apagar.html'
    success_url = reverse_lazy('visita')
    success_message = 'Agendamento excluído com sucesso!'