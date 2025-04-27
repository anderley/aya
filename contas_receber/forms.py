from datetime import timedelta

from django import forms

from core.models import Banco, Categoria, CentroCusto, MotivoExclusao
from empresas.models import Empresa
from fluxo_caixa.models import FluxoCaixa
from fornecedores.models import Fornecedor


class ContaReceberForm(forms.ModelForm):

    class CategoriaChoiceField(forms.ModelChoiceField):

        def label_from_instance(self, obj):
            return f"{obj.descricao} | {obj.tipo_lancamento}"

    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.none(),
        label="Empresa"
    )
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.none(),
        label="Fornecedor"
    )
    categoria = CategoriaChoiceField(
        queryset=Categoria.objects.all(),
        label="Categoria"
    )
    centro_custo = forms.ModelChoiceField(
        queryset=CentroCusto.objects.all(),
        required=False, label="Centro de Custo"
    )
    data_emissao = forms.DateField(
        widget=forms.DateInput(
            format="%d/%m/%Y", attrs={"type": "date", "max": ""}
        ),
        label="Data Emissão"
    )
    valor = forms.CharField(max_length=22, label="Valor Parcela")
    valor_moeda_estrangeira = forms.CharField(
        max_length=22, required=False, label="Moeda Estrangeira"
    )
    valor_cotacao = forms.CharField(
        max_length=6, required=False, label="Valor Cotação"
    )
    data_vencimento = forms.DateField(
        widget=forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"}),
        label="Data Vencimento"
    )
    data_pagamento = forms.DateField(
        widget=forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"}),
        required=False, label="Data Pagamento"
    )
    banco = forms.ModelChoiceField(
        queryset=Banco.objects.all().order_by("nome"),
        required=False, label="Banco"
    )
    projeto = forms.CharField(required=False, label="Projeto")
    forma_pagamento = forms.ChoiceField(
        choices=FluxoCaixa.FormasPagamentos.choices, label="Forma Pagamento"
    )
    num_documento = forms.CharField(required=False, label="Num. Documento")
    parcelas = forms.IntegerField(required=False, label="Parcelas")
    arquivo = forms.FileField(required=False, label="Arquivo")

    def __init__(self, *args, **kwargs):
        tenant_id = kwargs.pop("tenant_id")

        super().__init__(*args, **kwargs)

        self.fields["empresa"].queryset = Empresa.objects.filter(
            tenant_id=tenant_id
        )
        self.fields["fornecedor"].queryset = Fornecedor.objects.filter(
            tenant_id=tenant_id
        )

    def clean_valor(self):
        valor = self.cleaned_data["valor"]
        valor = valor.replace(".", "").replace(",", ".")

        return valor and float(valor)

    def clean_valor_moeda_estrangeira(self):
        valor_moeda_estrangeira = self.cleaned_data["valor_moeda_estrangeira"]

        if not valor_moeda_estrangeira:
            return None

        return valor_moeda_estrangeira

    def clean_valor_cotacao(self):
        valor_cotacao = self.cleaned_data["valor_cotacao"]

        if not valor_cotacao:
            return None

        return valor_cotacao

    def clean_parcelas(self):
        parcelas = self.cleaned_data["parcelas"]

        if not parcelas:
            return 1

        return parcelas

    def save(self, commit=True):
        parcelas = self.instance.parcelas

        instance = super().save(commit)
        parcela_pricipal_id = instance.pk

        for i in range(2, parcelas + 1):
            instance.pk = None
            instance.num_parcela = i
            instance.data_vencimento = instance.data_vencimento + timedelta(
                days=30
            )
            instance.parcela_principal = FluxoCaixa.objects.get(
                id=parcela_pricipal_id
            )
            instance.save()

        return instance

    class Meta:
        model = FluxoCaixa
        exclude = ["num_parcela", "parcela_principal"]


class ContaReceberUpdateForm(forms.ModelForm):

    class CategoriaChoiceField(forms.ModelChoiceField):

        def label_from_instance(self, obj):
            return f"{obj.descricao} | {obj.tipo_lancamento}"

    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.none(),
        label="Empresa", disabled=True
    )
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.none(),
        label="Fornecedor", disabled=True
    )
    categoria = CategoriaChoiceField(
        queryset=Categoria.objects.all(),
        label="Categoria", disabled=True
    )
    centro_custo = forms.ModelChoiceField(
        queryset=CentroCusto.objects.all(),
        required=False, label="Centro de Custo", disabled=True
    )
    data_emissao = forms.DateField(
        widget=forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"}),
        label="Data Emissão"
    )
    valor = forms.CharField(max_length=22, label="Valor")
    valor_moeda_estrangeira = forms.CharField(
        max_length=22, required=False, label="Moeda Estrangeira"
    )
    valor_cotacao = forms.CharField(
        max_length=6, required=False, label="Valor Cotação"
    )
    data_vencimento = forms.DateField(
        widget=forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"}),
        label="Data Vencimento"
    )
    data_pagamento = forms.DateField(
        widget=forms.DateInput(format="%d/%m/%Y", attrs={"type": "date"}),
        required=False, label="Data Pagamento"
    )
    banco = forms.ModelChoiceField(
        queryset=Banco.objects.all().order_by("nome"),
        required=False, label="Banco"
    )
    projeto = forms.CharField(
        required=False, label="Projeto", disabled=True
    )
    forma_pagamento = forms.ChoiceField(
        choices=FluxoCaixa.FormasPagamentos.choices, label="Forma Pagamento"
    )
    num_documento = forms.CharField(required=False, label="Num. Documento")
    parcelas = forms.IntegerField(
        required=False, label="Parcelas", disabled=True
    )
    arquivo = forms.FileField(required=False, label="Arquivo")
    parcela_principal = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )

    def clean_valor(self):
        valor = self.cleaned_data["valor"]
        valor = valor.replace(".", "").replace(",", ".")

        return valor and float(valor)

    def clean_valor_moeda_estrangeira(self):
        valor_moeda_estrangeira = self.cleaned_data["valor_moeda_estrangeira"]

        if not valor_moeda_estrangeira:
            return None

        return valor_moeda_estrangeira

    def clean_valor_cotacao(self):
        valor_cotacao = self.cleaned_data["valor_cotacao"]

        if not valor_cotacao:
            return None

        return valor_cotacao

    def clean_parcelas(self):
        parcelas = self.cleaned_data["parcelas"]

        if not parcelas:
            return 1

        return parcelas

    def clean_parcela_principal(self):
        parcela_principal = FluxoCaixa.objects.get(
            id=self.cleaned_data.get("parcela_principal")
        )
        return parcela_principal

    def __init__(self, *args, **kwargs):
        tenant_id = kwargs.pop("tenant_id")

        super().__init__(*args, **kwargs)

        self.fields["empresa"].queryset = Empresa.objects.filter(
            tenant_id=tenant_id
        )
        self.fields["fornecedor"].queryset = Fornecedor.objects.filter(
            tenant_id=tenant_id
        )

    class Meta:
        model = FluxoCaixa
        exclude = ["num_parcela"]


class ItemDeleteForm(forms.Form):
    motivo_exclusao = forms.ModelChoiceField(
        queryset=MotivoExclusao.objects.all()
    )
    items = forms.ModelMultipleChoiceField(
        queryset=FluxoCaixa.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class ContaReceberDeleteForm(forms.Form):
    motivo_exclusao = forms.ModelChoiceField(
        queryset=MotivoExclusao.objects.all()
    )
