# Generated by Django 5.1.6 on 2025-02-19 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='tipo_lancamento',
            field=models.CharField(default=None, max_length=100, unique=True, verbose_name='Tipo Lançamento'),
            preserve_default=False,
        ),
    ]
