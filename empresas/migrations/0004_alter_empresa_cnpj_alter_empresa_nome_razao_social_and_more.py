# Generated by Django 5.1.6 on 2025-02-16 10:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0003_alter_empresa_telefone_alter_empresa_whatsapp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='cnpj',
            field=models.CharField(max_length=18, unique=True, verbose_name='CNPJ'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='nome_razao_social',
            field=models.CharField(max_length=100, unique=True, verbose_name='Razão Social'),
        ),
        migrations.AddConstraint(
            model_name='empresa',
            constraint=models.UniqueConstraint(fields=('user', 'cnpj'), name='unique_empresa_user'),
        ),
    ]
