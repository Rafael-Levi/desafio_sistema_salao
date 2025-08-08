# agendamentos/forms.py
from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'profissional', 'inicio', 'duracao_minutos', 'status', 'observacoes']
        widgets = {
            'inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
