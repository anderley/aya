from django.db import models
from django.contrib.auth.models import User

from main.models import Estados


class Empresa(models.Model):
    tenant_id = models.UUIDField(db_index=True)
    nome = models.CharField(max_length=50, verbose_name='Nome')
    cnpj = models.CharField(max_length=18, unique=True, verbose_name='CNPJ')
    nome_razao_social = models.CharField(max_length=100, unique=True, verbose_name='Razão Social')
    im = models.CharField(max_length=10, null=True, blank=True, verbose_name='Insc. Municipal')
    ie = models.CharField(max_length=10, null=True, blank=True, verbose_name='Insc. Estadual')
    telefone = models.CharField(max_length=14, null=True, blank=True, verbose_name='Telefone')
    whatsapp = models.CharField(max_length=15, null=True, blank=True, verbose_name='Whatsapp')
    email = models.CharField(max_length=80, null=True, blank=True, verbose_name='E-mail')
    cep = models.CharField(max_length=9, null=True, blank=True, verbose_name='Cep')
    endereco = models.CharField(max_length=60, null=True, blank=True, verbose_name='Endereço')
    complemento = models.CharField(max_length=60, null=True, blank=True, verbose_name='Complemento')
    numero = models.CharField(max_length=5, null=True, blank=True, verbose_name='Número')
    bairro = models.CharField(max_length=80, null=True, blank=True, verbose_name='Bairro')
    estado = models.CharField(max_length=80, null=True, blank=True, choices=Estados.choices, verbose_name='Estado')
    cidade = models.CharField(max_length=80, null=True, blank=True, verbose_name='Cidade')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado')

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'empresas'
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
        constraints = [
            models.UniqueConstraint(fields=['tenant_id', 'cnpj'], name='unique_empresa_tenant') # noqa
        ]
