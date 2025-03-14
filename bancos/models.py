from django.db import models


class Banco(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "bancos"
        verbose_name = "banco"
        verbose_name_plural = "bancos"
