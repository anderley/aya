from django.db import models

from empresas.models import Empresa


class Estoque(models.Model):
    empresa = models.ForeignKey(
        Empresa, on_delete=models.DO_NOTHING, verbose_name="Empresa"
    )
    is_primeiro = models.BooleanField(blank=True, null=True, default=False, verbose_name="É primeiro")
    competencia = models.DateField(verbose_name="Competência")
    valor = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Valor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Deletado Em"
    )

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "estoques"
        verbose_name = "estoque"
        verbose_name_plural = "estoques"
        constraints = [
            models.UniqueConstraint(
                fields=["empresa", "is_primeiro"],
                condition=models.Q(is_primeiro=True),
                name="unique_empresa_primary_estoque"
            ),
            models.UniqueConstraint(
                fields=["empresa", "competencia"],
                name="unique_empresa_mes_estoque"
            )
        ]