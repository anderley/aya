from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document_number = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="CNPJ / CPF"
    )
    tenant_id = models.UUIDField(
        blank=True, null=True, db_index=True, verbose_name="Tenant ID"
    )

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'user_profile'
        verbose_name_plural = 'User Profile'
