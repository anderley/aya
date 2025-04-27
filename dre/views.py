from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from fluxo_caixa.models import FluxoCaixa
from core.models import Indicador
from .helpers import DREHelper


class DRETemplateView(LoginRequiredMixin, TemplateView):
    template_name = "dre/view.html"

    def get_context_data(self, **kwargs):
        competencia = self.request.GET.get("competencia", "data_emissao")
        context = super().get_context_data(**kwargs)
        context["data"] = DREHelper.get_data(
            list(
                FluxoCaixa.objects.filter(
                    empresa__tenant_id=self.request.user.userprofile.tenant_id,
                    deleted_at=None,
                ).order_by(competencia)
            ),
            list(
                Indicador.objects.all()
            ),
            competencia
        )

        return context
