import re
from django.db import models
from pessoa.models import Pessoa
# Create your models here.
class Proprietario(Pessoa):
    codigoProprietario = models.CharField('Código do Proprietário', max_length=10, unique=True) 

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.codigoProprietario:  
        
            iniciais = self.__class__.__name__[:2].upper()  
            finais = self.__class__.__name__[-2:].upper()   
        
        
            ultimo_proprietario = Proprietario.objects.order_by('-codigoProprietario').first()
        
            if ultimo_proprietario:  
                numero = int(ultimo_proprietario.codigoProprietario[2:-2]) + 1
            else:  
                numero = 1
            
        
            self.codigoProprietario = f"{iniciais}{numero:03d}{finais}"
    
        super().save(*args, **kwargs)  