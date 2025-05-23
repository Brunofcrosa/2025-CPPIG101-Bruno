from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Corretor
from .forms import CorretorModelForm

class CorretoresView(ListView):
    model = Corretor
    template_name = 'corretores.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(CorretoresView, self).get_queryset()
        
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum corretor encontrado com esse nome')

class CorretorAddView(SuccessMessageMixin, CreateView):
    model = Corretor
    form_class = CorretorModelForm
    template_name = 'corretor_form.html'
    success_url = reverse_lazy('corretor')
    success_message = 'corretor cadastrado com sucesso!'

class CorretorUpdateView(SuccessMessageMixin, UpdateView):
    model = Corretor
    form_class = CorretorModelForm
    template_name = 'corretor_form.html'
    success_url = reverse_lazy('corretor')
    success_message = 'corretor alterado com sucesso!'

class CorretorDeleteView(SuccessMessageMixin, DeleteView):
    model = Corretor
    template_name = 'corretor_apagar.html'
    success_url = reverse_lazy('corretor')
    success_message = 'corretor excluído com sucesso!'