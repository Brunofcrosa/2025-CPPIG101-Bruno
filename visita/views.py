from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Visita
from .forms import VisitaModelForm
from django.utils import timezone # Importar timezone

class VisitaView(PermissionRequiredMixin, ListView):
    permission_required = 'visita.view_visita'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
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
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_month = timezone.now().month
        current_year = timezone.now().year

        context['total_visita'] = Visita.objects.count()
        context['visitas_agendadas_mes'] = Visita.objects.filter(
            data__month=current_month,
            data__year=current_year
        ).count()
        # O modelo Visita não possui um campo de status para determinar "Visitas Concluídas".
        # Para um cálculo preciso, seria necessário adicionar um campo 'status' ao modelo Visita.
        context['visitas_concluidas_mes'] = 0 
        return context


class VisitaAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'visita.add_visita'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Visita
    form_class = VisitaModelForm
    template_name = 'visita_form.html'
    success_url = reverse_lazy('visita')
    success_message = 'Agendamento cadastrado com sucesso!'

class VisitaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'visita.change_visita'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Visita
    form_class = VisitaModelForm
    template_name = 'visita_form.html'
    success_url = reverse_lazy('visita')
    success_message = 'Agendamento alterado com sucesso!'

class VisitaDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'visita.delete_visita'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Visita
    template_name = 'visita_apagar.html'
    success_url = reverse_lazy('visita')
    success_message = 'Agendamento excluído com sucesso!'