import calendar
import locale

from datetime import date

from django import forms
from django.db import IntegrityError

from .models import Estoque
from empresas.models import Empresa
from core.models import MotivoExclusao


locale.setlocale(locale.LC_TIME, "pt_BR.utf8")


class EstoqueForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.none(), label="Empresa"
    )
    is_primeiro = forms.BooleanField(required=False, label="É primeiro")
    ano = forms.ChoiceField(
        choices=((y, y) for y in range(2025, 1950, -1)), label="Ano"
    )
    mes = forms.ChoiceField(
        choices=((idx, calendar.month_name[idx]) for idx in range(1, 13)), label="Mẽs"
    )
    valor = forms.CharField(max_length=22, label="Valor")

    def __init__(self, *args, **kwargs):
        tenant_id = kwargs.pop("tenant_id")

        super().__init__(*args, **kwargs)

        # Load dynamic fields
        self.fields["empresa"].queryset = Empresa.objects.filter(
            tenant_id=tenant_id
        )
    
    def clean_valor(self):
        valor = self.cleaned_data["valor"]
        valor = valor.replace(".", "").replace(",", ".")

        return valor and float(valor)
    
    def is_valid(self):
        is_valid =  super().is_valid()

        if is_valid:
            try:
                self.save()
            except IntegrityError as e:
                self.add_error(None, e)
                is_valid = False

        return is_valid
    
    def save(self, commit=True):
        print("passando save");
        ano = self.cleaned_data.get("ano")
        mes = self.cleaned_data.get("mes")

        self.instance.competencia = date(int(ano), int(mes), 1)

        return super().save(commit)
        

    class Meta:
        model = Estoque
        exclude = ["competencia"]


class ItemDeleteForm(forms.Form):
    motivo_exclusao = forms.ModelChoiceField(
        queryset=MotivoExclusao.objects.all()
    )
    items = forms.ModelMultipleChoiceField(
        queryset=Estoque.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class EstoqueDeleteForm(forms.Form):
    motivo_exclusao = forms.ModelChoiceField(
        queryset=MotivoExclusao.objects.all()
    )
