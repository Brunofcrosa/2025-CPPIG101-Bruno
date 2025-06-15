from django.db import models
from stdimage.models import StdImageField
from imovel.models import Imovel
from cliente.models import Cliente
# Create your models here.
class Visita(models.Model):
    corretor = models.ForeignKey('corretores.Corretor', on_delete=models.CASCADE, related_name='corretor', null=True)
    imovel = models.ForeignKey('imovel.Imovel', on_delete=models.CASCADE, related_name='imovel', null=True)
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, related_name='cliente', null=True)
    data = models.DateField('Data', help_text='Data da visita', null=True)
    codigoVisita = models.CharField('Código da Visita', max_length=10, unique=True, help_text='Código único da visita', default='Visita')

    class Meta:
        permissions = (('fechar_agendamento', 'Permite fazer o fechamento de uma visita'),)
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    