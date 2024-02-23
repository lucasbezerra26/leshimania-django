from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from django.db import models

from leishimaniaapp.core.models import BaseModelUuid


class MicroscopeSlide(BaseModelUuid):
    user = models.ForeignKey(
        User,
        verbose_name="Usuário",
        on_delete=models.CASCADE,
        related_name="microscope_slides",
    )
    slide_name = models.CharField("Nome da lâmina", max_length=255, unique=True)
    prediction_class = models.CharField(max_length=50)
    prediction_percentage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.slide_name

    class Meta:
        verbose_name = "Lâmina de microscópio"
        verbose_name_plural = "Lâminas de microscópio"
        ordering = ["slide_name"]


class MicroscopeImage(BaseModelUuid):
    image = models.ImageField("Imagem", upload_to="images/")
    prediction_class = models.CharField(max_length=50)
    prediction_percentage = models.FloatField(null=True, blank=True)
    microscope_slide = models.ForeignKey(
        MicroscopeSlide,
        verbose_name="Lâmina de microscópio",
        on_delete=models.CASCADE,
        related_name="images",
    )

    def __str__(self):
        return f"{self.microscope_slide.slide_name} - {self.id}"

    class Meta:
        verbose_name = "Imagem de microscópio"
        verbose_name_plural = "Imagens de microscópio"
        ordering = ["microscope_slide__slide_name"]
