from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from .cliente import Cliente
from .servico import Servico
from .profissional import Profissional

class Agendamento(models.Model):
    STATUS_AGENDADO = 'AGENDADO'
    STATUS_CONCLUIDO = 'CONCLUIDO'
    STATUS_CANCELADO = 'CANCELADO'
    STATUS_CHOICES = [
        (STATUS_AGENDADO, 'Agendado'),
        (STATUS_CONCLUIDO, 'Concluído'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name='agendamentos')
    profissional = models.ForeignKey(Profissional, on_delete=models.PROTECT, related_name='agendamentos')
    inicio = models.DateTimeField()  # data e hora de início
    duracao_minutos = models.PositiveIntegerField(help_text='Duração em minutos', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AGENDADO)
    observacoes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-inicio']
        indexes = [
            models.Index(fields=['inicio']),
            models.Index(fields=['status']),
            models.Index(fields=['profissional', 'inicio']),
        ]

    def __str__(self):
        return f"{self.cliente} - {self.servico} - {self.inicio.strftime('%Y-%m-%d %H:%M')}"

    @property
    def fim(self):
        dur = self.duracao_minutos or self.servico.duracao_minutos
        return self.inicio + timedelta(minutes=dur)

    def clean(self):
        if not self.duracao_minutos:
            self.duracao_minutos = self.servico.duracao_minutos

        inicio = self.inicio
        fim = self.fim
        
        window_start = inicio - timedelta(minutes=240)
        window_end = fim + timedelta(minutes=240)

        candidates = Agendamento.objects.filter(
            profissional=self.profissional,
            inicio__lt=window_end,
            inicio__gte=window_start
        ).exclude(pk=self.pk).filter(status__in=[self.STATUS_AGENDADO, self.STATUS_CONCLUIDO])

        for other in candidates:
            other_dur = other.duracao_minutos or other.servico.duracao_minutos
            other_start = other.inicio
            other_end = other_start + timedelta(minutes=other_dur)
            if (inicio < other_end) and (other_start < fim):
                raise ValidationError("Conflito de horário: o profissional já está ocupado nesse período.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
