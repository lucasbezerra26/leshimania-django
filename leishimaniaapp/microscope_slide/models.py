from django.db import models
from django.utils.translation import gettext_lazy as _

from leishimaniaapp.accounts.models import User
from leishimaniaapp.core.models import BaseModelUuid


class PredictionClass(models.TextChoices):
    POSITIVO = "pos", _("Positivo")
    NEGATIVO = "neg", _("Negativo")
    DESCONHECIDO = "unk", _("Desconhecido")


class TaskType(models.TextChoices):
    INCEPTION = "inception", _("LV Humana")
    YOLO = "yolo", _("LV Canina")
    NONE = "none", _("Nenhuma")


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
        "Classe de previsão",
        max_length=20,
        choices=PredictionClass.choices,
        default=None,
        null=True,
    )
    prediction_percentage = models.FloatField(
        "Porcentagem de previsão", null=True, blank=True
    )

    task_type = models.CharField(
        "Tipo de Classificação",
        max_length=10,
        choices=TaskType.choices,
        default="yolo",
    )

    def __str__(self):
        return self.slide_name

    class Meta:
        verbose_name = "Lâmina de microscópio"
        verbose_name_plural = "Lâminas de microscópio"
        ordering = ["slide_name"]


class MicroscopeImage(BaseModelUuid):

    PATH_RESULT = "microscope_images/results/"

    microscope_slide = models.ForeignKey(
        MicroscopeSlide,
        verbose_name="Lâmina de microscópio",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField("Imagem", upload_to="microscope_images/")
    image_result = models.ImageField(
        "Imagem", upload_to=PATH_RESULT, null=True, blank=True
    )
    prediction_class = models.CharField(
        "Classe de previsão",
        max_length=20,
        choices=PredictionClass.choices,
        default=None,
        null=True,
    )
    prediction_percentage = models.FloatField(
        "Porcentagem de previsão", null=True, blank=True
    )

    def __str__(self):
        return f"{self.microscope_slide.slide_name} - {self.image}"

    class Meta:
        verbose_name = "Imagem de microscópio"
        verbose_name_plural = "Imagens de microscópio"
        ordering = ["microscope_slide__slide_name"]

    def image_name(self):
        return self.image.name.split("/")[-1]

    def image_result_name(self):
        return self.image_result.name.split("/")[-1]
