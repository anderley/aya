from django.db import models
from django.utils.translation import gettext_lazy as _

from categorias.models import Categoria
from fornecedores.models import Fornecedor
from empresas.models import Empresa
from centro_custos.models import CentroCusto
from bancos.models import Banco


class FluxoCaixa(models.Model):

    class FormasPagamentos(models.TextChoices):
        BOLETO = "Boleto", _("Boleto")
        CARTAO_CREDTIO = "Cartão Crédito", _("Cartão Crédito")
        DEBITO = "Débito", _("Débito")
        PIX  = "Pix", _("Pix")

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
    banco = models.ForeignKey(Banco, null=True, on_delete=models.DO_NOTHING, verbose_name="Banco")
    projeto = models.CharField(max_length=50, null=True, verbose_name="Projeto")
    forma_pagamento = models.CharField(max_length=30, choices=FormasPagamentos.choices, null=True, verbose_name="Forma Pagamento")
    num_documento = models.CharField(max_length=50, null=True, default=None, verbose_name="Número Documento")
    num_parcela = models.IntegerField(null=True, default=1, verbose_name="Número Parcela")
    parcelas = models.IntegerField(null=True, default=1, verbose_name="Parcelas")
    arquivo = models.FileField(upload_to="aya/fluxo-caixa/arquivos", null=True, blank=True, verbose_name="Arquivo")
    parcela_principal = models.ForeignKey('FluxoCaixa', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Parcela Principal")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado Em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado Em")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Deletado Em")


    def __str__(self):
        return self.categoria.descricao

    class Meta:
        db_table = "fluxos_caixa"
        verbose_name = "fluxo_caixa"
        verbose_name_plural = "Fluxo Caixa"
