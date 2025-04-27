from django.db import models
from stdimage.models import StdImageField
# Create your models here.
class Visita(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    foto = StdImageField('Foto', upload_to='pessoas', delete_orphans=True, null=True, blank=True)
    endereco = models.CharField('Endereço', max_length=100, help_text='Endereço completo')
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome