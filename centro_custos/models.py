from django.db import models


class CentroCusto(models.Model):
    descricao = models.CharField(
        max_length=100, unique=True, verbose_name="Descrição"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = "centro_custos"
        verbose_name = "centro_custo"
        verbose_name_plural = "Centros Custos"
