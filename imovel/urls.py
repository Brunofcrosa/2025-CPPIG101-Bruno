from django.urls import path
from .views import ImovelView
from .views import ImovelAddView
from .views import ImovelUpdateView
from .views import ImovelDeleteView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('imovel/', ImovelView.as_view(), name='imovel'),
    path('imovel/adicionar/', ImovelAddView.as_view(), name='imovel_adicionar'),
    path('imovel/<int:pk>/editar/', ImovelUpdateView.as_view(), name='imovel_editar'),
    path('imovel/<int:pk>/apagar/', ImovelDeleteView.as_view(), name='imovel_apagar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)