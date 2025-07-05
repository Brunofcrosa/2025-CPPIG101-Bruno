from django.db import models
from pessoa.models import Pessoa
from stdimage.models import StdImageField

class Corretor(Pessoa):
    codigoCorretor = models.CharField('Código do Corretor', max_length=10, unique=True, help_text='Código único do corretor') 
    foto = StdImageField('Foto', upload_to='corretores', delete_orphans=True, blank=False, null=False)

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.codigoCorretor:  
            iniciais = self.__class__.__name__[:2].upper()  
            finais = self.__class__.__name__[-2:].upper()   
            ultimo_corretor = Corretor.objects.order_by('-codigoCorretor').first()
        
            if ultimo_corretor:  
                numero = int(ultimo_corretor.codigoCorretor[2:-2]) + 1
            else:  
                numero = 1
            self.codigoCorretor = f"{iniciais}{numero:03d}{finais}"
    
        super().save(*args, **kwargs)  