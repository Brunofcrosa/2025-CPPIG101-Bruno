from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Visita
from .forms import VisitaModelForm
from django.utils import timezone 
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
# Create your views here.
class VisitaView(PermissionRequiredMixin, ListView):
    permission_required = 'visita.view_visita'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Visita
    template_name = 'visitas.html'


    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(VisitaView, self).get_queryset()
        
        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum agendamento encontrado!')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_month = timezone.now().month
        current_year = timezone.now().year

        context['total_visita'] = Visita.objects.count()
        context['visitas_agendadas_mes'] = Visita.objects.filter(
            data__month=current_month,
            data__year=current_year
        ).count()
        context['visitas_concluidas_mes'] = 0 
        return context


class VisitaAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'visita.add_visita'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Visita
    form_class = VisitaModelForm
    template_name = 'visita_form.html'
    success_url = reverse_lazy('visita')
    success_message = 'Agendamento cadastrado com sucesso!'

   # def form_valid(self, form):
    #    response = super().form_valid(form)
        
       
      #  assunto = "Confirmação de Agendamento de Visita"
      #  template_html = "visita_confirmacao.html"
       # contexto = {'visita': self.object, 'cliente': self.object.cliente}
       # destinatario_email = self.object.cliente.email
        
       # html_content = render_to_string(template_html, contexto)
       # text_content = strip_tags(html_content) 

      #  email = EmailMultiAlternatives(
       #     assunto,
       #     text_content,
        #    settings.DEFAULT_FROM_EMAIL,
         #   [destinatario_email]
        #)
        #email.attach_alternative(html_content, "text/html")
        #email.send() 

        #return response

class VisitaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'visita.change_visita'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Visita
    form_class = VisitaModelForm
    template_name = 'visita_form.html'
    success_url = reverse_lazy('visita')
    success_message = 'Agendamento alterado com sucesso!'

    #def form_valid(self, form):
     #   response = super().form_valid(form)
        
      #  assunto = "Atualização de Agendamento de Visita"
       # template_html = "visita_confirmacao.html"
        #contexto = {'visita': self.object, 'cliente': self.object.cliente}
        #destinatario_email = self.object.cliente.email
        
        #html_content = render_to_string(template_html, contexto)
        #text_content = strip_tags(html_content)

        #email = EmailMultiAlternatives(
         #   assunto,
          #  text_content,
           # settings.DEFAULT_FROM_EMAIL,
           # [destinatario_email]
       # )
        #email.attach_alternative(html_content, "text/html")
        #email.send() 

        #return response

class VisitaDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'visita.delete_visita'
    permission_denied_message = 'Você não tem permissão para acessar esta página.'
    model = Visita
    template_name = 'visita_apagar.html'
    success_url = reverse_lazy('visita')
    success_message = 'Agendamento excluído com sucesso!'