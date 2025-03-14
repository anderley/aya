from datetime import datetime

from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from django.utils import timezone

from .models import FluxoCaixa


@receiver(post_save, sender=FluxoCaixa)
def update_parcelas(sender, instance, created, **kwargs):
    if(
        not instance.parcela_principal
        and instance.deleted_at
    ):
        fluxos_caixa = FluxoCaixa.objects.filter(
            parcela_principal=instance.id
        ).all()

        for fluxo_caixa in fluxos_caixa:
            fluxo_caixa.deleted_at = datetime.now()
            fluxo_caixa.save()
    elif(
        instance.deleted_at
    ):
        fluxos_caixa = FluxoCaixa.objects.filter(
            Q(parcela_principal=instance.parcela_principal.id)|Q(id=instance.parcela_principal.id),
            deleted_at=None
        ).order_by("num_parcela")
        
        for index, fluxo_caixa in enumerate(fluxos_caixa):
            fluxo_caixa.parcelas = len(fluxos_caixa)
            fluxo_caixa.num_parcela = index + 1
            fluxo_caixa.save()
