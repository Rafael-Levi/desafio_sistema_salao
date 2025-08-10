from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    duracao_minutos = models.PositiveIntegerField(default=60)  # duração padrão
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome