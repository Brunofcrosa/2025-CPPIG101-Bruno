from .models import Corretor

def total_corretores(request):
    return {
        'total_corretores': Corretor.objects.count()
    }