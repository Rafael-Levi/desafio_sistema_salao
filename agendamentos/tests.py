# agendamentos/tests.py
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Cliente, Servico, Profissional, Agendamento

class AgendamentoTestCase(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome='Cliente 1')
        self.servico = Servico.objects.create(nome='Corte', duracao_minutos=60, preco=50)
        self.prof = Profissional.objects.create(nome='Pro 1')

    def test_conflito_agendamento(self):
        inicio = timezone.now() + timedelta(days=1, hours=2)
        a1 = Agendamento.objects.create(
            cliente=self.cliente,
            servico=self.servico,
            profissional=self.prof,
            inicio=inicio
        )
        with self.assertRaises(Exception):
            Agendamento.objects.create(
                cliente=self.cliente,
                servico=self.servico,
                profissional=self.prof,
                inicio=inicio + timedelta(minutes=30)  # overlap
            )

