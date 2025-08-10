from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import cliente, servico, profissional, agendamento

class AgendamentoTestCase(TestCase):
    def setUp(self):
        self.cliente = cliente.Cliente.objects.create(nome='Cliente 1')
        self.servico = servico.Servico.objects.create(nome='Corte', duracao_minutos=60, preco=50)
        self.prof = profissional.Profissional.objects.create(nome='Pro 1')

    def test_conflito_agendamento(self):
        inicio = timezone.now() + timedelta(days=1, hours=2)
        a1 = agendamento.Agendamento.objects.create(
            cliente=self.cliente,
            servico=self.servico,
            profissional=self.prof,
            inicio=inicio
        )
        with self.assertRaises(Exception):
            agendamento.Agendamento.objects.create(
                cliente=self.cliente,
                servico=self.servico,
                profissional=self.prof,
                inicio=inicio + timedelta(minutes=30)  # overlap
            )

