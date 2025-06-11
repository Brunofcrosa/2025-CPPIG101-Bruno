from django.db import models
from stdimage.models import StdImageField
# Create your models here.
class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email', unique=True)
    telefone = models.CharField('Telefone', max_length=15)
    foto = StdImageField('Foto', upload_to='pessoas', delete_orphans=True, null=True, blank=True)
    endereco = models.CharField('Endereço', max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome