from django.urls import path
from .views import CorretorListView

urlpatterns = [
    path('corretores/', CorretorListView.as_view(), name='Corretor'),
]