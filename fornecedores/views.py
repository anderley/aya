from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Fornecedor
from .forms import FornecedorForm


class FornecedoresListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    paginate_by = 20
    template_name = "fornecedores/lista.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            tenant_id=self.request.user.userprofile.tenant_id
        ).order_by("-created_at")


class FornecedoresCreateView(
    LoginRequiredMixin, SuccessMessageMixin, CreateView
):
    form_class = FornecedorForm
    template_name = "fornecedores/form.html"
    success_url = reverse_lazy("listar_fornecedores")
    success_message = "Fornecedor cadastradp com sucesso."

    def post(self, request, *args, **kwargs):
        self.initial["tenant_id"] = request.user.userprofile.tenant_id

        return super().post(request, *args, **kwargs)


class FornecedoresUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = "fornecedores/form.html"
    success_url = reverse_lazy("listar_fornecedores")
    success_message = "Fornecedor atualizado com sucesso."


class FornecedoresDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Fornecedor
    template_name = "fornecedores/confirmar_exclusao.html"
    success_url = reverse_lazy("listar_fornecedores")
    success_message = "Fornecedor deletado com sucesso."
