from django.urls import path
from .views import TransacoesView, TransacaoAddView, TransacaoUpdateView, TransacaoDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('transacao/', TransacoesView.as_view(), name='transacao'),
    path('transacao/adicionar/', TransacaoAddView.as_view(), name='transacao_adicionar'),
    path('transacao/<int:pk>/editar/', TransacaoUpdateView.as_view(), name='transacao_editar'),
    path('transacao/<int:pk>/apagar/', TransacaoDeleteView.as_view(), name='transacao_apagar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)