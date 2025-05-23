from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import EmpresaForm
from .models import Empresa


class EmpresasListView(LoginRequiredMixin, ListView):
    model = Empresa
    paginate_by = 20
    template_name = "empresas/lista.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            tenant_id=self.request.user.userprofile.tenant_id
        ).order_by("-created_at")


class EmpresasCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = EmpresaForm
    template_name = "empresas/form.html"
    success_url = reverse_lazy("listar_empresas")
    success_message = "Empresa cadastrada com sucesso."

    def post(self, request, *args, **kwargs):
        self.initial["tenant_id"] = request.user.userprofile.tenant_id

        return super().post(request, *args, **kwargs)


class EmpresasUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = "empresas/form.html"
    success_url = reverse_lazy("listar_empresas")
    success_message = "Empresa atualizado com sucesso."


class EmpresasDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Empresa
    template_name = "empresas/confirmar_exclusao.html"
    success_url = reverse_lazy("listar_empresas")
    success_message = "Empresa deletado com sucesso."
