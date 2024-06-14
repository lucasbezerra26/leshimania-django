from django.urls import path
from .views import (
    MicroscopeSlideView,
    SlideClassificationView,
    HomeView,
    ListMicroscopeImageView,
)

urlpatterns = [
    path("laminas/", MicroscopeSlideView.as_view(), name="add_microscope_slide"),
    path(
        "imagens/<uuid:slide_id>/",
        ListMicroscopeImageView.as_view(),
        name="list_microscope_image",
    ),
    path(
        "classification/<int:slide_id>/",
        SlideClassificationView.as_view(),
        name="slide_classification1",
    ),
    path("", HomeView.as_view(), name="home"),
    path("", HomeView.as_view(), name="dataset"),
    path("", HomeView.as_view(), name="slide_classification"),
]
