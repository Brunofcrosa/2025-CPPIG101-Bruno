from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Imovel
from .forms import ImovelModelForm
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.utils import timezone 

class ImovelView(PermissionRequiredMixin, ListView):
    permission_required = 'imovel.view_imovel'
    permission_denied_message = 'Visualizar imóvel'
    model = Imovel
    template_name = 'imovel.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ImovelView, self).get_queryset()
        
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum imovel encontrado com esse nome')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_imoveis'] = Imovel.objects.count()
        context['imoveis_disponiveis_locacao'] = Imovel.objects.filter(disponivel_locacao=True).count()
        
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        context['imoveis_desatualizados'] = Imovel.objects.filter(last_updated__lt=six_months_ago).count()
        return context

class ImovelAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'imovel.add_imovel'
    permission_denied_message = 'Cadastrar imóvel'
    model = Imovel
    form_class = ImovelModelForm
    template_name = 'imovel_form.html'
    success_url = reverse_lazy('imovel')
    success_message = 'Imovel cadastrado com sucesso!'

class ImovelUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'imovel.change_imovel'
    permission_denied_message = 'Editar imóvel'
    model = Imovel
    form_class = ImovelModelForm
    template_name = 'imovel_form.html'
    success_url = reverse_lazy('imovel')
    success_message = 'Imovel alterado com sucesso!'

class ImovelDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'imovel.delete_imovel'
    permission_denied_message = 'Excluir imóvel'
    model = Imovel
    template_name = 'imovel_apagar.html'
    success_url = reverse_lazy('imovel')
    success_message = 'Imovel excluído com sucesso!'

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
            messages.error(request, "Não é possível excluir este imóvel pois há registros relacionados que o impedem.")
            return self.render_to_response(self.get_context_data(object=self.object))