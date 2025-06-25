# 2025-CPPIG101-Bruno/proprietarios/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Proprietario
from .forms import ProprietarioModelForm
from django.utils import timezone # Importar timezone para cálculos de data

class ProprietariosView(PermissionRequiredMixin, ListView):
    permission_required = 'proprietarios.view_proprietario'
    permission_denied_message = 'Você não tem permissão para acessar essa página.'
    model = Proprietario
    template_name = 'proprietarios.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()
        
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Nenhum Proprietario encontrado com esse nome')
            return Proprietario.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_month = timezone.now().month
        current_year = timezone.now().year

        context['total_proprietarios'] = Proprietario.objects.count()
        context['proprietarios_ativos'] = Proprietario.objects.count() # Considerando todos os proprietários como ativos, pois não há campo de status.
        # Para um cálculo preciso de "novos proprietários (mês)", seria necessário um campo 'data_cadastro' no modelo Pessoa.
        context['novos_proprietarios_mes'] = 0 
        
        return context

class ProprietarioAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'proprietarios.add_proprietario'
    permission_denied_message = 'Você não tem permissão para acessar essa página.'
    model = Proprietario
    form_class = ProprietarioModelForm
    template_name = 'proprietario_form.html'
    success_url = reverse_lazy('proprietario')
    success_message = 'Proprietario cadastrado com sucesso!'

class ProprietarioUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'proprietarios.change_proprietario'
    permission_denied_message = 'Você não tem permissão para acessar essa página.'
    model = Proprietario
    form_class = ProprietarioModelForm
    template_name = 'proprietario_form.html'
    success_url = reverse_lazy('proprietario')
    success_message = 'Proprietario alterado com sucesso!'

class ProprietarioDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'proprietarios.delete_proprietario'
    permission_denied_message = 'Você não tem permissão para acessar essa página.'
    model = Proprietario
    template_name = 'proprietario_apagar.html'
    success_url = reverse_lazy('proprietario')
    success_message = 'Proprietario excluído com sucesso!'