from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView

from core.models import MotivoExclusao

from .models import Auditoria


class AuditoriasListView(LoginRequiredMixin, ListView):
    model = Auditoria
    template_name = "audit/lista.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            tenant_id=self.request.user.userprofile.tenant_id
        )

        if "usuario" in self.request.GET and self.request.GET["usuario"]:
            queryset = queryset.filter(
                usuario=self.request.GET["usuario"]
            )
        if "motivo" in self.request.GET and self.request.GET["motivo"]:
            queryset = queryset.filter(
                motivo=self.request.GET["motivo"]
            )
        if "data_ini" in self.request.GET and self.request.GET["data_ini"]:
            queryset = queryset.filter(
                created_at__gte=self.request.GET["data_ini"]
            )
        if "data_end" in self.request.GET and self.request.GET["data_end"]:
            queryset = queryset.filter(
                created_at__lte=self.request.GET["data_end"]
            )
        if "acao" in self.request.GET and self.request.GET["acao"]:
            queryset = queryset.filter(
                acao=self.request.GET["acao"]
            )

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["usuarios"] = User.objects.filter(
            userprofile__tenant_id=self.request.user.userprofile.tenant_id
        )
        context["motivos_exclusao"] = MotivoExclusao.objects.all()
        context["acoes"] = Auditoria.Acao.choices

        return context
