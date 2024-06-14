from django.contrib import admin

from leishimaniaapp.microscope_slide.models import (
    Laboratory,
    MicroscopeSlide,
    MicroscopeImage,
)


@admin.register(MicroscopeSlide)
class MicroscopeSlideAdmin(admin.ModelAdmin):
    list_display = ["slide_name", "prediction_class", "prediction_percentage"]
    search_fields = ["slide_name", "prediction_class"]
    list_filter = ["prediction_class"]


@admin.register(MicroscopeImage)
class MicroscopeImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    pass
