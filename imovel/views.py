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

    def dispatch(self, request, *args, **kwargs):
        self.delete_imoveis_without_proprietarios()
        return super().dispatch(request, *args, **kwargs)
    
    def delete_imoveis_without_proprietarios(self):
        imoveis_to_delete = Imovel.objects.all()
        deleted_count = 0
        for imovel in imoveis_to_delete:
            if not imovel.has_proprietarios(): 
                imovel.delete()
                deleted_count += 1
        if deleted_count > 0:
            messages.info(self.request, f'{deleted_count} Imóvel sem proprietário foi automaticamente excluído.')

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