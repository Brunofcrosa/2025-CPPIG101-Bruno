
from .models import Imovel

def total_imoveis(request):
    return {
        'total_imoveis': Imovel.objects.count()
    }