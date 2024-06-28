from django.db import models

from leishimaniaapp.accounts.models import User
from leishimaniaapp.core.models import BaseModelUuid


class Laboratory(BaseModelUuid):
    name = models.CharField("Nome do Laboratório", max_length=255, unique=True)
    description = models.TextField("Descrição", blank=True, null=True)
    participants = models.ManyToManyField(
        User, verbose_name="Participantes", blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Laboratório"
        verbose_name_plural = "Laboratórios"


class MicroscopeSlide(BaseModelUuid):
    user = models.ForeignKey(
        User,
        verbose_name="Usuário",
        on_delete=models.SET_NULL,
        null=True,
        related_name="microscope_slides",
    )
    laboratory = models.ForeignKey(
        Laboratory,
        verbose_name="Laboratório",
        on_delete=models.SET_NULL,
        null=True,
        related_name="slides",
    )
    slide_name = models.CharField("Nome da lâmina", max_length=255, unique=True)
    prediction_class = models.CharField(
        "Classe de previsão", max_length=50, null=True, blank=True
    )
    prediction_percentage = models.FloatField(
        "Porcentagem de previsão", null=True, blank=True
    )

    def __str__(self):
        return self.slide_name

    class Meta:
        verbose_name = "Lâmina de microscópio"
        verbose_name_plural = "Lâminas de microscópio"
        ordering = ["slide_name"]


class MicroscopeImage(BaseModelUuid):
    microscope_slide = models.ForeignKey(
        MicroscopeSlide,
        verbose_name="Lâmina de microscópio",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField("Imagem", upload_to="microscope_images/")
    prediction_class = models.CharField(
        "Classe de previsão", max_length=50, null=True, blank=True
    )

    def __str__(self):
        return f"{self.microscope_slide.slide_name} - {self.image}"

    class Meta:
        verbose_name = "Imagem de microscópio"
        verbose_name_plural = "Imagens de microscópio"
        ordering = ["microscope_slide__slide_name"]
