from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Transacao
from .forms import TransacaoModelForm 
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

class TransacoesView(PermissionRequiredMixin, ListView):
    permission_required = 'transacao.view_transacao'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Transacao
    template_name = 'transacoes.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()
        
        if buscar:
            qs = qs.filter(codigoTransacao__icontains=buscar) 

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Nenhuma transação encontrada!')
            return Transacao.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_transacoes'] = Transacao.objects.count()
        context['transacoes_concluidas'] = Transacao.objects.filter(statusTransacao='Concluída').count()
        context['transacoes_pendentes'] = Transacao.objects.filter(statusTransacao='Pendente').count()
        return context

class TransacaoAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'transacao.add_transacao'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Transacao
    form_class = TransacaoModelForm 
    template_name = 'transacao_form.html'
    success_url = reverse_lazy('transacao')
    success_message = 'transacao cadastrado com sucesso!'

class TransacaoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'transacao.change_transacao'
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete() 
            messages.success(request, self.success_message)
            return self.get_success_url() 
        except ValidationError as e:
            messages.error(request, e.message)
            return self.render_to_response(self.get_context_data(object=self.object)) 
        except ProtectedError:
            messages.error(request, "Não é possível excluir esta transação pois há registros relacionados que o impedem.")
            return self.render_to_response(self.get_context_data(object=self.object))