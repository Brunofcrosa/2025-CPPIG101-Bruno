from django.views.generic import TemplateView
from imovel.models import Imovel
from cliente.models import Cliente
from corretores.models import Corretor
from visita.models import Visita
from transacao.models import Transacao
from django.db.models import Sum
from django.utils import timezone

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_imoveis'] = Imovel.objects.count()
        context['total_clientes'] = Cliente.objects.count()
        context['total_corretores'] = Corretor.objects.count()
        context['total_visitas'] = Visita.objects.filter(data__gte=timezone.now().date()).count()
        context['imoveis_recentes'] = Imovel.objects.order_by('-last_updated')[:4]
        context['visitas_recentes'] = Visita.objects.filter(data__gte=timezone.now().date()).order_by('data')[:4]
        current_month = timezone.now().month
        current_year = timezone.now().year
        vendas_mes = Transacao.objects.filter(
            dataTransacao__month=current_month,
            dataTransacao__year=current_year,
            statusTransacao='Concluída'
        )
        context['total_vendas_mes'] = vendas_mes.count()
        context['faturamento_mensal'] = vendas_mes.aggregate(total_faturamento=Sum('valorVenda'))['total_faturamento'] or 0
        corretores_scores = {}
        for corretor in Corretor.objects.all():
            vendas_corretor_mes = Transacao.objects.filter(
                codigoCorretor=corretor,
                dataTransacao__month=current_month,
                dataTransacao__year=current_year,
                statusTransacao='Concluída'
            ).count()
            visitas_corretor_mes = Visita.objects.filter(
                corretor=corretor,
                data__month=current_month,
                data__year=current_year
            ).count()
            
            score = (vendas_corretor_mes * 2) + visitas_corretor_mes
            corretores_scores[corretor] = {
                'score': score,
                'vendas_mes': vendas_corretor_mes,
                'faturado_mes': Transacao.objects.filter(
                    codigoCorretor=corretor,
                    dataTransacao__month=current_month,
                    dataTransacao__year=current_year,
                    statusTransacao='Concluída'
                ).aggregate(total_faturado=Sum('valorComissao'))['total_faturado'] or 0,
                'vendas_total': Transacao.objects.filter(
                    codigoCorretor=corretor,
                    statusTransacao='Concluída'
                ).count(),
            }
        
        corretor_destaque = None
        if corretores_scores:
            corretor_destaque = max(corretores_scores, key=lambda corretor: corretores_scores[corretor]['score'])
            context['corretor_destaque'] = corretor_destaque
            context['corretor_destaque_dados'] = corretores_scores[corretor_destaque]
        context['transacoes_recentes'] = Transacao.objects.order_by('-dataTransacao')[:5]
        return context