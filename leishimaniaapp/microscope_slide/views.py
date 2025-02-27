from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView

from .forms import MicroscopeSlideFormModal, MicroscopeImageForm
from .models import MicroscopeSlide, MicroscopeImage
from .tasks import process_image, process_image_yolo

from django.http import JsonResponse


class MicroscopeSlideView(LoginRequiredMixin, View):

    def get(self, request):
        form = MicroscopeSlideFormModal(user_filter=request.user)
        slides = MicroscopeSlide.objects.filter(laboratory__participants=request.user)
        return render(
            request,
            "microscope_slide/microscope_slide.html",
            {"form": form, "slides": slides},
        )

    def post(self, request):
        form = MicroscopeSlideFormModal(request.POST, user_filter=request.user)
        if form.is_valid():
            slide = form.save(commit=False)
            slide.user = request.user
            slide.save()
            return redirect("add_microscope_slide")
        return render(request, "microscope_slide/microscope_slide.html", {"form": form})


class ListMicroscopeImageView(LoginRequiredMixin, FormView):
    template_name = "microscope_slide/microscope_images.html"
    form_class = MicroscopeImageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slide_id = self.kwargs["slide_id"]
        context["images"] = MicroscopeImage.objects.filter(microscope_slide=slide_id)
        context["slide_name"] = MicroscopeSlide.objects.get(id=slide_id).slide_name
        context["slide_id"] = slide_id
        return context

    def post(self, request, *args, **kwargs):
        slide_id = self.kwargs["slide_id"]
        microscope_slide = get_object_or_404(MicroscopeSlide, id=slide_id)
        files = request.FILES.getlist("image")

        for file in files:
            slide_image = MicroscopeImage(microscope_slide=microscope_slide, image=file)
            slide_image.save()
            if microscope_slide.task_type == "yolo":
                process_image_yolo.delay(slide_image.id)
            else:
                process_image.delay(slide_image.id)

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            "list_microscope_image", kwargs={"slide_id": self.kwargs["slide_id"]}
        )


class SlideClassificationView(LoginRequiredMixin, View):
    def get(self, request, slide_id):
        slide = MicroscopeSlide.objects.get(id=slide_id)
        images = slide.images.all()
        return render(
            request, "add_image_form.html", {"slide": slide, "images": images}
        )


class CaptureImageView(LoginRequiredMixin, TemplateView):
    template_name = "microscope_slide/capture_image_vue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slide_id = self.kwargs["slide_id"]
        context["slide_name"] = MicroscopeSlide.objects.get(id=slide_id).slide_name
        context["slide_id"] = slide_id
        return context

    def post(self, request, *args, **kwargs):
        slide_id = self.kwargs["slide_id"]
        microscope_slide = get_object_or_404(MicroscopeSlide, id=slide_id)
        files = request.FILES.getlist("file")

        for file in files:
            slide_image = MicroscopeImage(microscope_slide=microscope_slide, image=file)
            slide_image.save()
        return JsonResponse({"status": "ok"})


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "microscope_slide/home.html")
