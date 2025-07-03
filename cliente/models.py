import re
from django.db import models
from pessoa.models import Pessoa
    
class Cliente(Pessoa):
    codigoCliente = models.CharField('Código do Cliente', max_length=10, unique=True, help_text='Código único do cliente')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.codigoCliente:
            nome_modelo = self.__class__.__name__
            prefixo = nome_modelo[0:2].upper()
            sufixo = nome_modelo[-2:].upper()

            padrao = re.compile(rf"^{prefixo}(\d+){sufixo}$")
            
            ultimo_numero_sequencial = 99
            
            todos_os_codigos_do_modelo = self.__class__.objects.filter(
                codigoCliente__startswith=prefixo,
                codigoCliente__endswith=sufixo
            ).values_list('codigoCliente', flat=True)

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
            self.codigoCliente = f"{prefixo}{proximo_numero_sequencial:03d}{sufixo}"
        
        super().save(*args, **kwargs)