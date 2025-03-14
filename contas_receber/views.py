from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from fluxo_caixa.models import FluxoCaixa
from categorias.models import Categoria
from centro_custos.models import CentroCusto
from motivos_exclusao.models import MotivoExclusao
from empresas.models import Empresa
from fornecedores.models import Fornecedor
from audit.models import Auditoria

from .forms import ContaReceberForm, ItemDeleteForm


def delete_items(request):
    if request.method == "POST":
        form = ItemDeleteForm(request.POST)

        if form.is_valid():
            total = len(form.cleaned_data["items"])
            items_to_delete = form.cleaned_data["items"]
            
            for item in items_to_delete:
                item.deleted_at = datetime.now()
                item.save()

                user = request.user

                Auditoria(
                    tenant_id=user.userprofile.tenant_id,
                    acao=Auditoria.Acao.EXCLUIDO,
                    motivo=form.cleaned_data["motivo_exclusao"],
                    registro=serializers.serialize("json", [item]),
                    usuario=user.email
                ).save()

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
            Q(empresa__tenant_id=self.request.user.userprofile.tenant_id),
            Q(deleted_at=None),
            Q(valor__gt=0)|Q(valor_moeda_estrangeira__gt=0)
        )

        if "empresa" in self.request.GET and self.request.GET["empresa"]:
            queryset = queryset.filter(
                empresa=self.request.GET["empresa"]
            )
        if "fornecedor" in self.request.GET and self.request.GET["fornecedor"]:
            queryset = queryset.filter(
                fornecedor=self.request.GET["fornecedor"]
            )
        if "categoria" in self.request.GET and self.request.GET["categoria"]:
            queryset = queryset.filter(
                categoria=self.request.GET["categoria"]
            )
        if "centro_custo" in self.request.GET and self.request.GET["centro_custo"]:
            queryset = queryset.filter(
                centro_custo=self.request.GET["centro_custo"]
            )
        if "data_vencimento_ini" in self.request.GET and self.request.GET["data_vencimento_ini"]:
            queryset = queryset.filter(
                data_vencimento__gte=self.request.GET["data_vencimento_ini"]
            )
        if "data_vencimento_end" in self.request.GET and self.request.GET["data_vencimento_end"]:
            queryset = queryset.filter(
                data_vencimento__lte=self.request.GET["data_vencimento_end"]
            )
        
        return queryset.order_by("data_vencimento")
    
    def get(self, request, *args, **kwargs):
        kwargs['tenant_id'] = request.user.userprofile.tenant_id

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categorias"] = Categoria.objects.all()
        context["centro_custos"] = CentroCusto.objects.all()
        context["motivos_exclusao"] = MotivoExclusao.objects.all()
        context["empresas"] = Empresa.objects.filter(
            tenant_id=self.request.user.userprofile.tenant_id
        )
        context["fornecedores"] = Fornecedor.objects.filter(
            tenant_id=self.request.user.userprofile.tenant_id
        )

        return context


class ContasReceberCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ContaReceberForm
    template_name = "contas_receber/form.html"
    success_url = reverse_lazy("listar_contas_receber")
    success_message = "Conta a receber criada com sucesso."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant_id'] = self.request.user.userprofile.tenant_id

        return kwargs


class ContasReceberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FluxoCaixa
    form_class = ContaReceberForm
    template_name = "contas_receber/form.html"
    success_url = reverse_lazy("listar_contas_receber")
    success_message = "Conta a receber atualizada com sucesso."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant_id'] = self.request.user.userprofile.tenant_id

        return kwargs
    

class ContasReceberDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = FluxoCaixa
    template_name = "contas_receber/confirmar_exclusao.html"
    success_url = reverse_lazy("listar_contas_receber")
    success_message = "Conta a receber deletada com sucesso."

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted_at = datetime.now()
        self.object.save()

        user = self.request.user

        Auditoria(
            tenant_id=user.userprofile.tenant_id,
            acao=Auditoria.Acao.EXCLUIDO,
            motivo=form.cleaned_data["motivo_exclusao"],
            registro=serializers.serialize("json", [self.object]),
            usuario=user.email
        ).save()

        return HttpResponseRedirect(success_url)
