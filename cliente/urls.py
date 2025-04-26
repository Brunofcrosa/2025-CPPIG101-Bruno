from django.urls import path
from .views import ClientesView, ClienteAddView, ClienteUpdateView, ClienteDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('clientes/', ClientesView.as_view(), name='cliente'),
    path('cliente/adicionar/', ClienteAddView.as_view(), name='cliente_adicionar'),
    path('cliente/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('cliente/<int:pk>/apagar/', ClienteDeleteView.as_view(), name='cliente_apagar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)