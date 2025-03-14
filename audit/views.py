from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Auditoria


class AuditoriasListView(LoginRequiredMixin, ListView):
    model = Auditoria
    template_name = "audit/lista.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            tenant_id=self.request.user.userprofile.tenant_id
        )

        return queryset
