# Generated by Django 5.1.6 on 2025-02-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo_caixa', '0004_alter_fluxocaixa_forma_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='fluxocaixa',
            name='num_parcela',
            field=models.IntegerField(null=True, verbose_name='Número Parcela'),
        ),
        migrations.AlterField(
            model_name='fluxocaixa',
            name='parcelas',
            field=models.IntegerField(null=True, verbose_name='Parcelas'),
        ),
    ]
