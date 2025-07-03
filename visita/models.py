import re
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
    codigoVisita = models.CharField('Código da Visita', max_length=10, unique=True, help_text='Código único da visita') 

    class Meta:
        permissions = (('fechar_agendamento', 'Permite fazer o fechamento de uma visita'),)
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def save(self, *args, **kwargs):
        if not self.codigoVisita:
            nome_modelo = self.__class__.__name__
            prefixo = nome_modelo[0:2].upper()
            sufixo = nome_modelo[-2:].upper()

            padrao = re.compile(rf"^{prefixo}(\d+){sufixo}$")
            
            ultimo_numero_sequencial = 99
            
            todos_os_codigos_do_modelo = self.__class__.objects.filter(
                codigoVisita__startswith=prefixo,
                codigoVisita__endswith=sufixo
            ).values_list('codigoVisita', flat=True)

            for codigo in todos_os_codigos_do_modelo:
                correspondencia = padrao.match(codigo)
                if correspondencia:
                    try:
                        numero_atual = int(correspondencia.group(1))
                        if numero_atual > ultimo_numero_sequencial:
                            ultimo_numero_sequencial = numero_atual
                    except ValueError:
                        pass
            
            proximo_numero_sequencial = ultimo_numero_sequencial + 1
            self.codigoVisita = f"{prefixo}{proximo_numero_sequencial:03d}{sufixo}"
        
        super().save(*args, **kwargs)