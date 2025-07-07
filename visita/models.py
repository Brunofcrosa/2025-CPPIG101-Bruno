from django.db import models
import re
class Visita(models.Model):
    corretor = models.ForeignKey('corretores.Corretor', on_delete=models.CASCADE, related_name='corretor_visitas', verbose_name='Corretor:', null=True)
    imovel = models.ForeignKey('imovel.Imovel', on_delete=models.CASCADE, related_name='imovel_visitas', verbose_name='Imóvel:', null=True)
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, related_name='cliente_visitas', verbose_name='Cliente:', null=True)
    data = models.DateField('Data:', null=True)
    hora = models.TimeField('Hora:', null=True, blank=True) 
    codigoVisita = models.CharField('Código da Visita', max_length=10, unique=True, help_text='Código único da visita')

    class Meta:
        permissions = (('fechar_agendamento', 'Permite fazer o fechamento de uma visita'),)
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'

    def __str__(self):
        return self.codigoVisita 

    def save(self, *args, **kwargs):
        if not self.codigoVisita:
            iniciais = self.__class__.__name__[:2].upper()
            finais = self.__class__.__name__[-2:].upper()

            ultima_visita = Visita.objects.order_by('-codigoVisita').first()

            if ultima_visita:
                match = re.match(r'^[A-Z]{2}(\d+)[A-Z]{2}$', ultima_visita.codigoVisita)
                if match:
                    numero = int(match.group(1)) + 1
                else:
                    numero = 1 
            else:
                numero = 1

            self.codigoVisita = f"{iniciais}{numero:03d}{finais}"

        super().save(*args, **kwargs)