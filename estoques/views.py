from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from empresas.models import Empresa
from core.models import MotivoExclusao

from .models import Estoque
from .forms import EstoqueForm, EstoqueDeleteForm, ItemDeleteForm


def delete_items(request):
    if request.method == "POST":
        form = ItemDeleteForm(request.POST)

        if form.is_valid():
            total = len(form.cleaned_data["items"])
            items_to_delete = form.cleaned_data["items"]

            for item in items_to_delete:
                item.deleted_at = datetime.now()
                item.save()


            messages.success(
                request, f"{total} estoques deletado com sucesso!"
            )
    else:
        form = ItemDeleteForm()

    return redirect("listar_estoques")  # Redirect after deletion


class EstoqueCreateView(
    LoginRequiredMixin, SuccessMessageMixin, CreateView
):
    form_class = EstoqueForm
    template_name = "estoques/form.html"
    success_url = reverse_lazy("listar_estoques")
    success_message = "Estoque criada com sucesso."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant_id'] = self.request.user.userprofile.tenant_id

        return kwargs

    def form_invalid(self, form):
        print("passando form_invalid");
        for e in form.non_field_errors():
            print(e)
            print("unique_empresa_mes_estoque" in e)
            if "unique_empresa_primary_estoque" in e:
                messages.error(self.request, "Primeiro estoque já registrado para essa empresa!")
            elif "unique_empresa_mes_estoque" in e:
                messages.error(self.request, "Estoque já registrado para esse mês e empresa!")
        return super().form_invalid(form)


class EstoqueDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Estoque
    form_class = EstoqueDeleteForm
    template_name = "estoques/confirmar_exclusao.html"
    success_url = reverse_lazy("listar_estoques")
    success_message = "Estoque deletado com sucesso."

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deleted_at = datetime.now()
        self.object.save()

        return HttpResponseRedirect(success_url)


class EstoqueListView(LoginRequiredMixin, ListView):
    model = Estoque
    template_name = "estoques/lista.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            empresa__tenant_id=self.request.user.userprofile.tenant_id,
            deleted_at=None
        )

        if "empresa" in self.request.GET and self.request.GET["empresa"]:
            queryset = queryset.filter(
                empresa=self.request.GET["empresa"]
            )
        if (
            "competencia_ini" in self.request.GET
            and self.request.GET["competencia_ini"]
        ):
            queryset = queryset.filter(
                competencia__gte=self.request.GET["competencia_ini"]
            )
        if (
            "competencia_end" in self.request.GET
            and self.request.GET["competencia_end"]
        ):
            queryset = queryset.filter(
                competencia__lte=self.request.GET["competencia_end"]
            )

        return queryset.order_by("competencia")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["empresas"] = Empresa.objects.filter(
            tenant_id=self.request.user.userprofile.tenant_id
        )
        context["motivos_exclusao"] = MotivoExclusao.objects.all()

        return context


class EstoqueUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Estoque
    form_class = EstoqueForm
    template_name = "estoques/form.html"
    success_url = reverse_lazy("listar_estoques")
    success_message = "Estoque atualizada com sucesso."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant_id'] = self.request.user.userprofile.tenant_id

        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        estoque = self.get_object()

        initial["ano"] = estoque.competencia.year
        initial["mes"] = estoque.competencia.month

        return initial
    
    def form_invalid(self, form):
        print("passando form_invalid");
        for e in form.non_field_errors():
            print(e)
            print("unique_empresa_mes_estoque" in e)
            if "unique_empresa_primary_estoque" in e:
                messages.error(self.request, "Primeiro estoque já registrado para essa empresa!")
            elif "unique_empresa_mes_estoque" in e:
                messages.error(self.request, "Estoque já registrado para esse mês e empresa!")
        return super().form_invalid(form)
