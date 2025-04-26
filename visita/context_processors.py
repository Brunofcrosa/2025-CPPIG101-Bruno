from .models import Visita

def total_visitas(request):
    return {
        'total_visitas': Visita.objects.count()
    }