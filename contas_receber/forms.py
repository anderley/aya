from datetime import timedelta

from django import forms
from django.db.models import Q

from fluxo_caixa.models import FluxoCaixa, FORMAS_PAGAMENTO
from empresas.models import Empresa
from fornecedores.models import Fornecedor
from categorias.models import Categoria
from centro_custos.models import CentroCusto


class ContaReceberForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.none(),
        label="Empresa"
    )
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.none(),
        label="Fornecedor"
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        label="Categoria"
    )
    centro_custo = forms.ModelChoiceField(
        queryset=CentroCusto.objects.all(),
        required=False, label="Centro de Custo"
    )
    data_emissao = forms.DateField(widget=forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"}), label="Data Emissão")
    valor = forms.CharField(max_length=22, label="Valor")
    valor_moeda_estrangeira = forms.CharField(max_length=22, required=False, label="Moeda Estrangeira")
    valor_cotacao = forms.CharField(max_length=6, required=False, label="Valor Cotação")
    data_vencimento = forms.DateField(widget=forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"}), label="Data Vencimento")
    data_pagamento = forms.DateField(widget=forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"}), required=False, label="Data Pagamento")
    conta_corrente = forms.CharField(required=False, label="Conta Corrente")
    projeto = forms.CharField(required=False, label="Projeto")
    forma_pagamento = forms.ChoiceField(choices=FORMAS_PAGAMENTO, label="Forma Pagamento")
    num_documento = forms.CharField(required=False, label="Num. Documento")
    parcelas = forms.IntegerField(required=False, label="Parcelas")
    arquivo = forms.FileField(required=False, label="Arquivo")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")

        super().__init__(*args, **kwargs)

        self.fields["empresa"].queryset = Empresa.objects.filter(
            user=user
        )
        self.fields["fornecedor"].queryset = Fornecedor.objects.filter(
            user=user
        )
    
    def clean_valor (self):
        valor = self.cleaned_data["valor"]
        valor = valor.replace(".", "").replace(",", ".")
        
        return valor and float(valor)
    
    def clean_valor_moeda_estrangeira (self):
        valor_moeda_estrangeira = self.cleaned_data["valor_moeda_estrangeira"]
        
        if not valor_moeda_estrangeira:
            return None

        return valor_moeda_estrangeira
    
    def clean_valor_cotacao (self):
        valor_cotacao = self.cleaned_data["valor_cotacao"]
        
        if not valor_cotacao:
            return None

        return valor_cotacao
    
    def clean_parcelas (self):
        parcelas = self.cleaned_data["parcelas"]
        
        if not parcelas:
            return 1

        return parcelas

    def save(self, commit=True):
        is_update = self.instance.pk
        parcelas = self.instance.parcelas

        instance = super().save(commit)
        
        if not is_update:
            for i in range(2, parcelas + 1):
                instance.pk=None
                instance.num_parcela=i
                instance.data_vencimento=instance.data_vencimento + timedelta(days=30)
                instance.save()
        
        return instance

    class Meta:
        model = FluxoCaixa
        exclude = ["num_parcela"]


class ItemDeleteForm(forms.Form):
    items = forms.ModelMultipleChoiceField(
        queryset=FluxoCaixa.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
