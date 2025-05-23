from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Imovel
from .forms import ImovelModelForm

class ImovelView(ListView):
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
    

class ImovelAddView(SuccessMessageMixin, CreateView):
    model = Imovel
    form_class = ImovelModelForm
    template_name = 'imovel_form.html'
    success_url = reverse_lazy('imovel')
    success_message = 'Imovel cadastrado com sucesso!'

class ImovelUpdateView(SuccessMessageMixin, UpdateView):
    model = Imovel
    form_class = ImovelModelForm
    template_name = 'imovel_form.html'
    success_url = reverse_lazy('imovel')
    success_message = 'Imovel alterado com sucesso!'

class ImovelDeleteView(SuccessMessageMixin, DeleteView):
    model = Imovel
    template_name = 'imovel_apagar.html'
    success_url = reverse_lazy('imovel')
    success_message = 'Imovel excluído com sucesso!'