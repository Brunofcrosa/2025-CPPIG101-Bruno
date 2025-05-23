from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Proprietario
from .forms import ProprietarioModelForm

class ProprietariosView(ListView):
    model = Proprietario
    template_name = 'proprietarios.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ProprietariosView, self).get_queryset()
        
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum Proprietario encontrado com esse nome')

class ProprietarioAddView(SuccessMessageMixin, CreateView):
    model = Proprietario
    form_class = ProprietarioModelForm
    template_name = 'proprietario_form.html'
    success_url = reverse_lazy('proprietario')
    success_message = 'Proprietario cadastrado com sucesso!'

class ProprietarioUpdateView(SuccessMessageMixin, UpdateView):
    model = Proprietario
    form_class = ProprietarioModelForm
    template_name = 'proprietario_form.html'
    success_url = reverse_lazy('proprietario')
    success_message = 'Proprietario alterado com sucesso!'

class ProprietarioDeleteView(SuccessMessageMixin, DeleteView):
    model = Proprietario
    template_name = 'proprietario_apagar.html'
    success_url = reverse_lazy('proprietario')
    success_message = 'Proprietario excluído com sucesso!'