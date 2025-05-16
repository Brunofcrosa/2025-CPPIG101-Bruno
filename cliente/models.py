from django.db import models
# Create your models here.
from pessoa.models import Pessoa
    
class Cliente(Pessoa):
    codigoCliente = models.CharField('Código do Cliente', max_length=10, unique=True, help_text='Código único do cliente')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome