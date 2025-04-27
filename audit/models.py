from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import MotivoExclusao


class Auditoria(models.Model):

    class Acao(models.TextChoices):
        CRIADO = "Criado", _("Criado")
        EDITADO = "Editado", _("Editado")
        EXCLUIDO = "Excluído", _("Excluído")

    tenant_id = models.UUIDField(db_index=True)
    acao = models.CharField(
        max_length=10, choices=Acao.choices,
        default=Acao.CRIADO, verbose_name="Ação"
    )
    motivo = models.ForeignKey(
        MotivoExclusao, on_delete=models.DO_NOTHING, verbose_name="Motivo"
    )
    registro = models.JSONField(verbose_name="Registro")
    usuario = models.CharField(max_length=100, verbose_name="Usuário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    class Meta:
        db_table = "auditorias"
        verbose_name = "auditoria"
        verbose_name_plural = "Auditorias"
