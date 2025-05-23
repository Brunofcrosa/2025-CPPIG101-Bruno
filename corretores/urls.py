from django.urls import path
from .views import CorretoresView, CorretorAddView, CorretorUpdateView, CorretorDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('corretores/', CorretoresView.as_view(), name='corretor'),
    path('corretor/adicionar/', CorretorAddView.as_view(), name='corretor_adicionar'),
    path('corretor/<int:pk>/editar/', CorretorUpdateView.as_view(), name='corretor_editar'),
    path('corretor/<int:pk>/apagar/', CorretorDeleteView.as_view(), name='corretor_apagar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)