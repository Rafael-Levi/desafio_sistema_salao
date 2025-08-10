from django.db import models
from django.contrib.auth.models import User

class Profissional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profissional_profile')
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.user:
            return f"{self.nome} ({self.user.username})"
        return self.nome
