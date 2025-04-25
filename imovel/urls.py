from django.urls import path
from . views import ImovelListView

urlpatterns = [
    path('imovel/', ImovelListView.as_view(), name='Imovel'),
]