from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Transacao
from .forms import TransacaoModelForm

class TransacoesView(PermissionRequiredMixin, ListView):
    permission_required = 'transacao.view_transacao'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Transacao
    template_name = 'transacoes.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(TransacoesView, self).get_queryset()
        
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum transacao encontrado com esse nome')

class TransacaoAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'transacao.add_transacao'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Transacao
    form_class = TransacaoModelForm
    template_name = 'transacao_form.html'
    success_url = reverse_lazy('transacao')
    success_message = 'transacao cadastrado com sucesso!'

class TransacaoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'transacao.update_transacao'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Transacao
    form_class = TransacaoModelForm
    template_name = 'transacao_form.html'
    success_url = reverse_lazy('transacao')
    success_message = 'transacao alterado com sucesso!'

class TransacaoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'transacao.delete_transacao'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Transacao
    template_name = 'transacao_apagar.html'
    success_url = reverse_lazy('transacao')
    success_message = 'transacao excluído com sucesso!'