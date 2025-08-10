from django import forms
from ..models import agendamento

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = agendamento.Agendamento
        fields = ['cliente', 'servico', 'profissional', 'inicio', 'duracao_minutos', 'status', 'observacoes']
        widgets = {
            'inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
