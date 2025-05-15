from django.views.generic import TemplateView
from imovel.models import Imovel
from cliente.models import Cliente
from corretor.models import Corretor
from visita.models import Visita

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_imoveis'] = Imovel.objects.count()
        context['imoveis_recentes'] = Imovel.objects.all()[:4]
        context['total_clientes'] = Cliente.objects.count()
        context['total_corretores'] = Corretor.objects.count()
        context['total_visitas'] = Visita.objects.count()
        context['visitas_recentes'] = Visita.objects.all()[:4]

        return context