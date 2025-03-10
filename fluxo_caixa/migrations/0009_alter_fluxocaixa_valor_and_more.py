# Generated by Django 5.1.6 on 2025-03-04 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo_caixa', '0008_alter_fluxocaixa_num_documento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fluxocaixa',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='fluxocaixa',
            name='valor_cotacao',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=19, null=True, verbose_name='Cotação Moeda'),
        ),
        migrations.AlterField(
            model_name='fluxocaixa',
            name='valor_moeda_estrangeira',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=19, null=True, verbose_name='Moeda Estrangeira'),
        ),
    ]
