from django.db import models
from pessoa.models import Pessoa
from stdimage.models import StdImageField
# Create your models here.
class Corretor(Pessoa):
    codigoCorretor = models.CharField('Código do Corretor', max_length=10, unique=True, help_text='Código único do corretor', default='CORRETOR')
    foto = StdImageField('Foto', upload_to='corretores', delete_orphans=True, blank=False, null=False)

    def __str__(self):
        return self.nome