# Generated by Django 5.1.6 on 2025-02-23 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo_caixa', '0005_fluxocaixa_num_parcela_alter_fluxocaixa_parcelas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fluxocaixa',
            name='valor_cotacao',
            field=models.FloatField(null=True, verbose_name='Cotação Moeda'),
        ),
        migrations.AlterField(
            model_name='fluxocaixa',
            name='valor_moeda_estrangeira',
            field=models.FloatField(null=True, verbose_name='Moeda Estrangeira'),
        ),
    ]
