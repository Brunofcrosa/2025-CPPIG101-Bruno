from django.shortcuts import render
from .models import Cliente
from django.views.generic import ListView
# Create your views here.

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes.html'
