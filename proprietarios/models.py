from django.db import models
# Create your models here.
from pessoa.models import Pessoa
    
class Proprietario(Pessoa):
    codigoProprietario = models.CharField('Código do Proprietário', max_length=10, unique=True, help_text='Código único do proprietário', default='PROPRIETARIO')
    
    class Meta:
        verbose_name = 'Proprietario'
        verbose_name_plural = 'Proprietarios'

    def __str__(self):
        return self.nome