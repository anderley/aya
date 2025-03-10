from django.db import models


class TipoLancamento(models.Model):
    descricao = models.CharField(max_length=100, unique=True, verbose_name="Descricao")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = "tipo_lancamentos"
        verbose_name = "tipo_lancamento"
        verbose_name_plural = "tipo_lancamentos"

