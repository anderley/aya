from django.db import models
from categorias.models import Categoria
from fornecedores.models import Fornecedor
from empresas.models import Empresa
from centro_custos.models import CentroCusto


FORMAS_PAGAMENTO = [
    ("Boleto", "Boleto"),
    ("Cartão Crédito", "Cartão Crédito"),
    ("Débito", "Débito"),
    ("Pix", "Pix"),
]

class FluxoCaixa(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    data_emissao = models.DateField(verbose_name="Data Emissão")
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.DO_NOTHING, verbose_name="Fornecedor"
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.DO_NOTHING, verbose_name="Categoria"
    )
    centro_custo = models.ForeignKey(
        CentroCusto, null=True, on_delete=models.DO_NOTHING, verbose_name="Centro de Custo"
    )
    valor = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Valor")
    valor_moeda_estrangeira = models.DecimalField(max_digits=19, decimal_places=2, null=True, default=None, verbose_name="Moeda Estrangeira")
    valor_cotacao = models.DecimalField(max_digits=19, decimal_places=2, null=True, default=None, verbose_name="Cotação Moeda")
    data_vencimento = models.DateField(verbose_name="Data Vencimento")
    data_pagamento = models.DateField(null=True, verbose_name="Data Pagamento")
    conta_corrente = models.CharField(max_length=50, null=True, verbose_name="Conta Corrente")
    projeto = models.CharField(max_length=50, null=True, verbose_name="Projeto")
    forma_pagamento = models.CharField(max_length=30, choices=FORMAS_PAGAMENTO, null=True, verbose_name="Forma Pagamento")
    num_documento = models.CharField(max_length=50, null=True, default=None, verbose_name="Número Documento")
    num_parcela = models.IntegerField(null=True, default=1, verbose_name="Número Parcela")
    parcelas = models.IntegerField(null=True, default=1, verbose_name="Parcelas")
    arquivo = models.FileField(upload_to="aya/fluxo-caixa/arquivos", null=True, verbose_name="Arquivo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado")

    def __str__(self):
        return self.categoria.descricao

    class Meta:
        db_table = "fluxos_caixa"
        verbose_name = "fluxo_caixa"
        verbose_name_plural = "fluxo_caixa"