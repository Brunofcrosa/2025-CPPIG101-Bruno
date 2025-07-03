from django.db import models, transaction
from django.core.exceptions import ValidationError
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
            iniciais = self.__class__.__name__[:2].upper()  
            finais = self.__class__.__name__[-2:].upper()   
            ultimo_cliente = Cliente.objects.order_by('-codigoCliente').first()
        
            if ultimo_cliente:  
                numero = int(ultimo_cliente.codigoCliente[2:-2]) + 1
            else:  
                numero = 1
        
            self.codigoCliente = f"{iniciais}{numero:03d}{finais}"
    
        super().save(*args, **kwargs)  