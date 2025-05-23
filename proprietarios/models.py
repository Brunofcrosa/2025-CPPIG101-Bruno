from django.db import models
from pessoa.models import Pessoa
# Create your models here.
class Proprietario(Pessoa):
    codigoProprietario = models.IntegerField('Código do Proprietário', help_text='Código do proprietário', unique=True, null=True, blank=True)

    def __str__(self):
        return self.nome