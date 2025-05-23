from django.db import models
from pessoa.models import Pessoa
# Create your models here.
class Transacao(Pessoa):
    codigoTransacao = models.CharField('Código do Transacao', max_length=10, unique=True, help_text='Código único do Transacao', default='Transacao')

    def __str__(self):
        return self.nome