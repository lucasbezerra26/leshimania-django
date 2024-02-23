import uuid

from django.db import models

# Create your models here.


class BaseModelUuid(models.Model):
    id = models.UUIDField(
        verbose_name="Indentificador",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(verbose_name="Criado às", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Atualizado às", auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
