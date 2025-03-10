from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Empresa
from .forms import EmpresaForm


class EmpresasListView(LoginRequiredMixin, ListView):
    model = Empresa
    paginate_by = 20
    template_name = "empresas/lista.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user
        ).order_by("-created_at")


class EmpresasCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = EmpresaForm
    template_name = "empresas/form.html"
    success_url = reverse_lazy("listar_empresas")
    success_message = "Empresa cadastrada com sucesso."

    def post(self, request, *args, **kwargs):
        self.initial["user_id"] = request.user.id

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
