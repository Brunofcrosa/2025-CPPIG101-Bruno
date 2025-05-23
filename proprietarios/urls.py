from django.urls import path
from .views import ProprietariosView, ProprietarioAddView, ProprietarioUpdateView, ProprietarioDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('proprietarios/', ProprietariosView.as_view(), name='proprietario'),
    path('proprietario/adicionar/', ProprietarioAddView.as_view(), name='proprietario_adicionar'),
    path('proprietario/<int:pk>/editar/', ProprietarioUpdateView.as_view(), name='proprietario_editar'),
    path('proprietario/<int:pk>/apagar/', ProprietarioDeleteView.as_view(), name='proprietario_apagar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)