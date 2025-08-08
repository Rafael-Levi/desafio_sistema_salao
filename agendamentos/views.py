from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Agendamento
from .forms import AgendamentoForm
from django.db.models import Prefetch
from django.shortcuts import render
from django import forms
from .reports import concluido_por_servico
from django.utils import timezone
from datetime import datetime, timedelta

class AgendamentoListView(ListView):
    model = Agendamento
    paginate_by = 20
    template_name = 'agendamentos/agendamento_list.html'
    context_object_name = 'agendamentos'

    def get_queryset(self):
        # use select_related para evitar N+1
        qs = super().get_queryset().select_related('cliente', 'servico', 'profissional')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(cliente__nome__icontains=q)
        return qs


class AgendamentoCreateView(CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/agendamento_form.html'
    success_url = reverse_lazy('agendamentos:list')


class AgendamentoUpdateView(UpdateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/agendamento_form.html'
    success_url = reverse_lazy('agendamentos:list')


class AgendamentoDeleteView(DeleteView):
    model = Agendamento
    template_name = 'agendamentos/agendamento_confirm_delete.html'
    success_url = reverse_lazy('agendamentos:list')


class AgendamentoDetailView(DetailView):
    model = Agendamento
    template_name = 'agendamentos/agendamento_detail.html'


class RelatorioForm(forms.Form):
    start = forms.DateField(required=True, widget=forms.DateInput(attrs={'type':'date'}))
    end = forms.DateField(required=True, widget=forms.DateInput(attrs={'type':'date'}))

def relatorio_servicos(request):
    form = RelatorioForm(request.GET or None)
    data = []
    if form.is_valid():
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end, datetime.max.time())
        data = concluido_por_servico(Agendamento.objects.all(), start_dt, end_dt)
    else:
        end_dt = timezone.now()
        start_dt = end_dt - timedelta(days=30)
        data = concluido_por_servico(Agendamento.objects.all(), start_dt, end_dt)
        form = RelatorioForm(initial={'start': start_dt.date(), 'end': end_dt.date()})

    return render(request, 'agendamentos/relatorio_servicos.html', {'form': form, 'data': data})