# Generated by Django 5.1.6 on 2025-02-16 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empresa',
            old_name='whataspp',
            new_name='whatsapp',
        ),
    ]
