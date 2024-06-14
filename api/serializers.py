from rest_framework import serializers

from leishimaniaapp.microscope_slide.models import MicroscopeImage


class MicroscopeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroscopeImage
        fields = [
            "microscope_slide",
            "image",
            "prediction_class",
            "prediction_percentage",
        ]
