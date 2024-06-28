from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MicroscopeImage, MicroscopeSlide


@receiver(post_save, sender=MicroscopeImage)
def update_microscope_slide(sender, instance, **kwargs):
    slide = instance.microscope_slide
    if instance.prediction_class == "Positivo":
        slide.prediction_class = "Positivo"
        slide.save(update_fields=["prediction_class"])
