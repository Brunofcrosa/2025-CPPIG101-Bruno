from django.db import models
from pessoa.models import Pessoa
# Create your models here.
class Corretor(Pessoa):
    codigoCorretor = models.CharField('Código do Corretor', max_length=10, unique=True, help_text='Código único do corretor', default='CORRETOR')

    def __str__(self):
        return self.nome