from django.shortcuts import render
from .models import Visita
from django.views.generic import ListView
# Create your views here.

class VisitaListView(ListView):
    model = Visita
    template_name = 'visitas.html'
