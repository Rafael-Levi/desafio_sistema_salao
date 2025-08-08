from django import forms
from .models import Agendamento, Servico, Profissional, Cliente

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'profissional', 'inicio', 'duracao_minutos', 'status', 'observacoes']
        widgets = {
            'inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
