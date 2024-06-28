from django.urls import path
from .views import (
    MicroscopeSlideView,
    SlideClassificationView,
    HomeView,
    ListMicroscopeImageView,
    CaptureImageView,
)

urlpatterns = [
    path("laminas/", MicroscopeSlideView.as_view(), name="add_microscope_slide"),
    path(
        "imagens/<uuid:slide_id>/",
        ListMicroscopeImageView.as_view(),
        name="list_microscope_image",
    ),
    path(
        "imagens/captura-automatica/<uuid:slide_id>/",
        CaptureImageView.as_view(),
        name="capture_image_auto",
    ),
    path(
        "classification/<int:slide_id>/",
        SlideClassificationView.as_view(),
        name="slide_classification1",
    ),
    path("", HomeView.as_view(), name="home"),
]
