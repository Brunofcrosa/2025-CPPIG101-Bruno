from django.db import models
from stdimage.models import StdImageField
from proprietarios.models import Proprietario

class Imovel(models.Model):  
    nome = models.CharField(max_length=100)  
    codigoImovel = models.CharField('Código do Imóvel', max_length=10, unique=True, help_text='Código único do imóvel', default='Imovel')
    foto = StdImageField('Foto', upload_to='pessoas', delete_orphans=True, null=True, blank=True)  
    endereco = models.CharField('Endereço', max_length=100, help_text='Endereço completo')
    proprietario = models.ManyToManyField(Proprietario, verbose_name='Proprietário', help_text='Selecione o proprietário do imóvel')

    class Meta:  
        verbose_name = 'Imóvel'  
        verbose_name_plural = 'Imóveis'  

    def __str__(self):  
        return self.nome