from datetime import datetime

from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from audit.models import Auditoria
from motivos_exclusao.models import MotivoExclusao
from usuarios.middleware import get_current_user
from .models import FluxoCaixa


@receiver(pre_save, sender=FluxoCaixa)
def audit_diff_fluxo_caixa(sender, instance, **kwargs):
    user = get_current_user()

    if user and instance.pk:  # Only set on update
        old_instance = sender.objects.get(pk=instance.pk)  # Get old data
        changes = []
        fields_diff = [
            "data_emissao", "valor", "valor_moeda_estrangeira",
            "valor_cotacao", "data_vencimento", "data_pagamento",
            "banco", "projeto", "forma_pagamento", "num_documento",
            "arquivo"
        ]

        for field in fields_diff:
            old_value = getattr(old_instance, field)
            new_value = getattr(instance, field)
            if old_value != new_value:  # Check for changes
                changes.append(
                    f"'{field}' mudou de '{old_value}' para '{new_value}'"
                )

        if changes:
            Auditoria(
                tenant_id=instance.empresa.tenant_id,
                acao=Auditoria.Acao.EDITADO,
                motivo=MotivoExclusao.objects.get(id=2),
                registro="<br> ".join(changes),  # Store changes as string,
                usuario=user.email
            ).save()


@receiver(post_save, sender=FluxoCaixa)
def update_fluxo_caixa(sender, instance, created, **kwargs):
    if getattr(instance, '_processing', False):
        return  # Prevent infinite loop

    if (
        not instance.parcela_principal
        and instance.deleted_at
    ):
        fluxos_caixa = sender.objects.filter(
            parcela_principal=instance.id
        ).all()

        for fluxo_caixa in fluxos_caixa:
            fluxo_caixa.deleted_at = datetime.now()
            fluxo_caixa.save()
    else:
        parcela_principal_id = (
            instance.parcela_principal.id
            if instance.parcela_principal
            else instance.id
        )

        fluxos_caixa = sender.objects.filter(
            Q(parcela_principal=parcela_principal_id)
            | Q(id=parcela_principal_id),
            deleted_at=None
        ).order_by("num_parcela")

        for index, fluxo_caixa in enumerate(fluxos_caixa):
            if instance.deleted_at:
                fluxo_caixa.parcelas = len(fluxos_caixa)
                fluxo_caixa.num_parcela = index + 1
            fluxo_caixa.data_emissao = instance.data_emissao
            fluxo_caixa.parcela_principal_id = parcela_principal_id
            fluxo_caixa._processing = True
            fluxo_caixa.save(update_fields=[
                "parcelas", "num_parcela",
                "data_emissao", "parcela_principal_id"
            ])
            fluxo_caixa._processing = False
