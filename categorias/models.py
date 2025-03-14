from django.db import models

from tipo_lancamentos.models import TipoLancamento


class Categoria(models.Model):
    descricao = models.CharField(
        max_length=100, unique=True, verbose_name="Descrição"
    )
    tipo_lancamento = models.ForeignKey(
        TipoLancamento, on_delete=models.DO_NOTHING,
        verbose_name="Tipo Lançamento"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = "categorias"
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
