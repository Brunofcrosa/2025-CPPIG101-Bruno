from django.db import models

# Create your models here.
class Corretor(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    endereco = models.TextField()

    def __str__(self):
        return self.nome