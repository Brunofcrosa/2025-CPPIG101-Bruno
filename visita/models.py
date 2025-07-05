from django.db import models
from stdimage.models import StdImageField
from imovel.models import Imovel
from cliente.models import Cliente

class Visita(models.Model):
    corretor = models.ForeignKey('corretores.Corretor', on_delete=models.CASCADE, related_name='corretor', null=True)
    imovel = models.ForeignKey('imovel.Imovel', on_delete=models.CASCADE, related_name='imovel', null=True)
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, related_name='cliente', null=True)
    data = models.DateField('Data', help_text='Data da visita', null=True)
    hora = models.TimeField('Hora', help_text='Hora da visita', null=True, blank=True) 
    codigoVisita = models.CharField('Código da Visita', max_length=10, unique=True, help_text='Código único da visita')

    class Meta:
        permissions = (('fechar_agendamento', 'Permite fazer o fechamento de uma visita'),)
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'

    def save(self, *args, **kwargs):
        if not self.codigoVisita:

            iniciais = self.__class__.__name__[:2].upper()
            finais = self.__class__.__name__[-2:].upper()


            ultima_visita = Visita.objects.order_by('-codigoVisita').first()

            if ultima_visita:
                numero = int(ultima_visita.codigoVisita[2:-2]) + 1
            else:
                numero = 1


            self.codigoVisita = f"{iniciais}{numero:03d}{finais}"

        super().save(*args, **kwargs)