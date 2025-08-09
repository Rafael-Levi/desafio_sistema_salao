from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Agendamento, Profissional, Cliente
from .forms import AgendamentoForm, ClienteForm
from .reports import concluido_por_servico
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponseBadRequest,HttpResponse
import io
import pandas as pd
from django.db.models import F


@login_required
@permission_required('agendamentos.add_cliente', raise_exception=True)
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agendamentos:clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'agendamentos/cliente_form.html', {'form': form, 'title': 'Adicionar Cliente'})

@login_required
@permission_required('agendamentos.change_cliente', raise_exception=True)
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'agendamentos/cliente_form.html', {'form': form, 'title': 'Editar Cliente'})

@login_required
@permission_required('agendamentos.view_cliente', raise_exception=True)
def clientes_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'agendamentos/clientes_list.html', {'clientes': clientes})


def is_recepcionista_or_admin(user):
    return user.is_superuser or user.groups.filter(name="Recepcionista").exists()

@login_required
def home(request):
    user = request.user

    if user.is_superuser or user.groups.filter(name="Dono").exists():
        return redirect('/admin/')

    if user.groups.filter(name="Recepcionista").exists():
        agendamentos = Agendamento.objects.select_related('cliente', 'servico', 'profissional').all()
        return render(request, 'agendamentos/home_recepcionista.html', {'agendamentos': agendamentos})

    if user.groups.filter(name="Profissional").exists():
        prof = None
        try:
            prof = Profissional.objects.get(user=user)
        except Profissional.DoesNotExist:
            try:
                nome = user.get_full_name() or user.username
                prof = Profissional.objects.get(nome__iexact=nome)
            except Profissional.DoesNotExist:
                prof = None

        if prof:
            agendamentos = Agendamento.objects.select_related('cliente', 'servico').filter(profissional=prof)
        else:
            agendamentos = Agendamento.objects.none()
        return render(request, 'agendamentos/home_profissional.html', {'agendamentos': agendamentos, 'profissional': prof})

    return render(request, 'agendamentos/home_default.html')


class AgendamentoListView(LoginRequiredMixin, ListView):
    model = Agendamento
    paginate_by = 20
    template_name = 'agendamentos/agendamento_list.html'
    context_object_name = 'agendamentos'

    def get_queryset(self):
        qs = super().get_queryset().select_related('cliente', 'servico', 'profissional')
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='Recepcionista').exists():
            return qs
        if user.groups.filter(name='Profissional').exists():
            try:
                prof = Profissional.objects.get(user=user)
            except Profissional.DoesNotExist:
                try:
                    prof = Profissional.objects.get(nome__iexact=user.get_full_name() or user.username)
                except Profissional.DoesNotExist:
                    return Agendamento.objects.none()
            return qs.filter(profissional=prof)
        return Agendamento.objects.none()


class AgendamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'agendamentos.add_agendamento'
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/agendamento_form.html'
    success_url = reverse_lazy('agendamentos:list')


class AgendamentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'agendamentos.change_agendamento'
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/agendamento_form.html'
    success_url = reverse_lazy('agendamentos:list')


class AgendamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'agendamentos.delete_agendamento'
    model = Agendamento
    template_name = 'agendamentos/agendamento_confirm_delete.html'
    success_url = reverse_lazy('agendamentos:list')


class AgendamentoDetailView(LoginRequiredMixin, DetailView):
    model = Agendamento
    template_name = 'agendamentos/agendamento_detail.html'


@login_required
def alterar_status_agendamento(request, pk):
    """
    Altera o status de um agendamento.
    - Somente POST é aceito.
    - Profissional só pode alterar seus próprios agendamentos.
    - Recepcionista e Admin podem alterar qualquer agendamento.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Apenas POST permitido.")

    novo_status = request.POST.get('status')
    allowed_status = [s[0] for s in Agendamento.STATUS_CHOICES]
    if novo_status not in allowed_status:
        return HttpResponseBadRequest("Status inválido.")

    agendamento = get_object_or_404(Agendamento, pk=pk)
    user = request.user

    if user.groups.filter(name='Profissional').exists():
        try:
            prof = Profissional.objects.get(user=user)
        except Profissional.DoesNotExist:
            return redirect('agendamentos:home')
        if agendamento.profissional != prof:
            return redirect('agendamentos:home')

    agendamento.status = novo_status
    agendamento.save()
    return redirect('agendamentos:home')


# Relatório
from django import forms
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


@login_required
def relatorio_servicos_download(request):

    start = request.GET.get('start')
    end = request.GET.get('end')
    if not start or not end:
        return HttpResponseBadRequest("Parâmetros 'start' e 'end' são obrigatórios no formato YYYY-MM-DD.")

    try:
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.strptime(end, '%Y-%m-%d').date()
    except Exception:
        return HttpResponseBadRequest("Formato de data inválido. Use YYYY-MM-DD.")

    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())

    # Query otimizada — traz apenas campos necessários
    qs = Agendamento.objects.select_related('servico', 'profissional', 'cliente').filter(
        inicio__gte=start_dt, inicio__lte=end_dt
    )

    rows = qs.values(
        'id',
        'inicio',
        'duracao_minutos',
        'status',
        servico_nome=F('servico__nome'),
        servico_duracao=F('servico__duracao_minutos'),
        servico_preco=F('servico__preco'),
        profissional_nome=F('profissional__nome'),
        cliente_nome=F('cliente__nome'),
    )

    df = pd.DataFrame(list(rows))

    # Se não há dados, retornar um excel simples com aviso
    if df.empty:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            pd.DataFrame([{'message': 'Nenhum dado no período selecionado.'}]).to_excel(writer, index=False, sheet_name='Resumo')
        output.seek(0)
        filename = f"relatorio_servicos_{start}_{end}.xlsx"
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    for col in df.select_dtypes(include=['datetimetz']).columns:
        df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)


    df['duracao_calc'] = df.apply(
        lambda r: r['duracao_minutos'] if r['duracao_minutos'] not in (None, 0) else r.get('servico_duracao', None),
        axis=1
    )

    # insights
    total_concluidos = int((df['status'] == 'CONCLUIDO').sum())
    total_cancelados = int((df['status'] == 'CANCELADO').sum())
    total_agendados = int((df['status'] == 'AGENDADO').sum())

    concluidos = df[df['status'] == 'CONCLUIDO']
    total_por_prof = (concluidos.groupby('profissional_nome')
                      .size().reset_index(name='total_concluidos')
                      .sort_values('total_concluidos', ascending=False))

    top_servicos = (concluidos.groupby('servico_nome')
                    .size().reset_index(name='total')
                    .sort_values('total', ascending=False))

    media_dur_serv = (df.groupby('servico_nome')['duracao_calc']
                      .mean().reset_index(name='duracao_media_minutos'))

    df['dia'] = pd.to_datetime(df['inicio']).dt.date
    por_dia = df.groupby('dia').size().reset_index(name='total')

    # Monta Excel em memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        
        df[['id','inicio','profissional_nome','cliente_nome','servico_nome','status','duracao_calc']].to_excel(writer, index=False, sheet_name='RawData')

        resumo = pd.DataFrame([
            {'metric':'total_concluidos','value': total_concluidos},
            {'metric':'total_cancelados','value': total_cancelados},
            {'metric':'total_agendados','value': total_agendados},
            {'metric':'period_start','value': start},
            {'metric':'period_end','value': end},
        ])
        resumo.to_excel(writer, index=False, sheet_name='Resumo')

        total_por_prof.to_excel(writer, index=False, sheet_name='Concluidos_por_Profissional')
        top_servicos.to_excel(writer, index=False, sheet_name='Top_Servicos')
        media_dur_serv.to_excel(writer, index=False, sheet_name='Media_Duracao_Por_Servico')
        por_dia.to_excel(writer, index=False, sheet_name='Agendamentos_por_Dia')

    output.seek(0)
    filename = f"relatorio_servicos_{start}_{end}.xlsx"
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
