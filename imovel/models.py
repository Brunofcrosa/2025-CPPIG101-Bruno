from django.db import models
from stdimage.models import StdImageField
from proprietarios.models import Proprietario

class Imovel(models.Model):  
    nome = models.CharField(max_length=100)  
    codigoImovel = models.CharField('Código do Imóvel', max_length=10, help_text='Código do imóvel')
    foto = StdImageField('Foto', upload_to='pessoas', delete_orphans=True, null=True, blank=True)  
    endereco = models.CharField('Endereço', max_length=100, help_text='Endereço completo')
    proprietario = models.ForeignKey('proprietarios.Proprietario', on_delete=models.CASCADE, related_name='proprietario_imovel', null=True)

    class Meta:  
        verbose_name = 'Imóvel'  
        verbose_name_plural = 'Imóveis'  

    def __str__(self):  
        return self.nome