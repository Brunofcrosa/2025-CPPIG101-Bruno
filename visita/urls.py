from django.urls import path
from .views import VisitaListView

urlpatterns = [
    path('visitas/', VisitaListView.as_view(), name='Visita'),
]