from django.db import models
from django.utils.translation import gettext_lazy as _


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


class Indicador(models.Model):

    class TipoIndicador(models.TextChoices):
        DRE = "DRE", _("DRE")
        DASH = "Dash", _("Dash")

    descricao = models.CharField(
        max_length=100, unique=True, verbose_name="Descricao"
    )
    tipo = models.CharField(max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    def __str__(self):
        return self.descricao
    
    def get_tipo_list(self):
        return self.tipo.split(',') if self.tipo else []

    class Meta:
        db_table = "indicadores"
        verbose_name = "indicador"
        verbose_name_plural = "Indicador"


class TipoLancamento(models.Model):
    indicador = models.ForeignKey(
        Indicador, on_delete=models.DO_NOTHING,
        verbose_name="Indicador"
    )
    descricao = models.CharField(
        max_length=100, unique=True, verbose_name="Descricao"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = "tipo_lancamentos"
        verbose_name = "tipo_lancamento"
        verbose_name_plural = "Tipos Lançamento"


class Categoria(models.Model):
    tipo_lancamento = models.ForeignKey(
        TipoLancamento, on_delete=models.DO_NOTHING,
        verbose_name="Tipo Lançamento"
    )
    descricao = models.CharField(
        max_length=100, unique=True, verbose_name="Descrição"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = "categorias"
        verbose_name = "categoria"
        verbose_name_plural = "categorias"


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


class MotivoExclusao(models.Model):
    descricao = models.CharField(
        max_length=100, unique=True, verbose_name="Descricao"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = "motivos_exclusao"
        verbose_name = "motivo_exclusao"
        verbose_name_plural = "Motivos Exclusão"
