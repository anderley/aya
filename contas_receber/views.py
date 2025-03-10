from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect


from fluxo_caixa.models import FluxoCaixa
from categorias.models import Categoria
from centro_custos.models import CentroCusto

from .forms import ContaReceberForm, ItemDeleteForm


def delete_items(request):
    if request.method == "POST":
        form = ItemDeleteForm(request.POST)

        if form.is_valid():
            total = len(form.cleaned_data['items'])
            items_to_delete = form.cleaned_data["items"]
            items_to_delete.delete()
            messages.success(request, f"{total} contas a receber deletado com sucesso!")
    else:
        form = ItemDeleteForm()

    return redirect("listar_contas_receber")  # Redirect after deletion


class ContasReceberListView(LoginRequiredMixin, ListView):
    model = FluxoCaixa
    template_name = "contas_receber/lista.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            Q(empresa__user=self.request.user),
            Q(valor__gt=0)|Q(valor_moeda_estrangeira__gt=0)
        )

        if "categoria" in self.request.GET and self.request.GET["categoria"]:
            queryset = queryset.filter(
                categoria=self.request.GET["categoria"]
            )
        if "centro_custo" in self.request.GET and self.request.GET["centro_custo"]:
            queryset = queryset.filter(
                centro_custo=self.request.GET["centro_custo"]
            )
        
        return queryset.order_by("data_vencimento")   
    
    def get(self, request, *args, **kwargs):
        kwargs['user'] = request.user

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categorias"] = Categoria.objects.all()
        context["centro_custos"] = CentroCusto.objects.all()

        return context


class ContasReceberCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ContaReceberForm
    template_name = "contas_receber/form.html"
    success_url = reverse_lazy("listar_contas_receber")
    success_message = "Conta a receber criada com sucesso."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


class ContasReceberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FluxoCaixa
    form_class = ContaReceberForm
    template_name = "contas_receber/form.html"
    success_url = reverse_lazy("listar_contas_receber")
    success_message = "Conta a receber atualizada com sucesso."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs
    

class ContasReceberDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = FluxoCaixa
    template_name = "contas_receber/confirmar_exclusao.html"
    success_url = reverse_lazy("listar_contas_receber")
    success_message = "Conta a receber deletada com sucesso."
