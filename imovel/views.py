from django.shortcuts import render
from .models import Imovel
from django.views.generic import ListView, CreateView
# Create your views here.

class ImovelListView(ListView):
    model = Imovel
    template_name = 'imovel.html'

class ImovelAddView(CreateView):
    model = Imovel
    template_name = 'Imovel_adicionar.html'
