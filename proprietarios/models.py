from django.db import models
from pessoa.models import Pessoa
# Create your models here.
class Proprietario(Pessoa):
    codigoProprietario = models.CharField('Código do Proprietario', max_length=10, unique=True, help_text='Código único do Proprietario', default='Proprietario')

    def __str__(self):
        return self.nome