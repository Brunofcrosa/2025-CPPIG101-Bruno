from django.shortcuts import render
from .models import Corretor
from django.views.generic import ListView
# Create your views here.

class CorretorListView(ListView):
    model = Corretor
    template = 'corretor.html'