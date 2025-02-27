from django.db import models


class MLModel(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nome do modelo
    version = models.CharField(max_length=20, default="1.0")  # Versão do modelo
    model_type = models.CharField(
        max_length=50,
        choices=[
            ("cnn", "CNN"),
            ("vit", "Vision Transformer"),
            ("custom", "Custom"),
        ],
    )
    accuracy = models.FloatField(default=0.0)  # Precisão do modelo treinado
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Indica se o modelo está ativo
    file = models.FileField(
        upload_to="models/", null=True, blank=True
    )  # Arquivo do modelo (se necessário)

    def __str__(self):
        return f"{self.name} (v{self.version})"


class Prediction(models.Model):
    image = models.ForeignKey(
        "core.Image", on_delete=models.CASCADE
    )  # Referência à imagem (assumindo que existe um app 'core' com um modelo de imagens)
    model = models.ForeignKey(
        MLModel, on_delete=models.CASCADE
    )  # Modelo utilizado na predição
    result = models.JSONField(
        default=dict
    )  # Resultado da predição (pode ser um dicionário com classes e probabilidades)
    processed_at = models.DateTimeField(auto_now_add=True)  # Data de processamento

    def __str__(self):
        return f"Predição {self.id} - {self.image.id} usando {self.model.name}"
