from django.urls import path
from .views import VisitaView, VisitaAddView, VisitaUpdateView, VisitaDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('visitas/', VisitaView.as_view(), name='visita'),
    path('visitas/adicionar/', VisitaAddView.as_view(), name='visita_adicionar'),
    path('visitas/<int:pk>/editar/', VisitaUpdateView.as_view(), name='visita_editar'),
    path('visitas/<int:pk>/apagar/', VisitaDeleteView.as_view(), name='visita_apagar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)