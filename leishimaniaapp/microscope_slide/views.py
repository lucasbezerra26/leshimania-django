import pickle

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView, CreateView, FormView
import joblib

from .helpers import verify_image_upload
from .models import MicroscopeSlide, MicroscopeImage, Laboratory
from .forms import MicroscopeSlideFormModal, MicroscopeImageForm
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import model_from_json
from tensorflow.keras.applications.inception_v3 import preprocess_input
import os
import numpy as np


class MicroscopeSlideView(View):

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


class ListMicroscopeImageView(FormView):
    template_name = "microscope_slide/microscope_images.html"
    form_class = MicroscopeImageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slide_id = self.kwargs["slide_id"]
        context["images"] = MicroscopeImage.objects.filter(microscope_slide=slide_id)
        context["slide_name"] = MicroscopeSlide.objects.get(id=slide_id).slide_name
        context["slide_id"] = slide_id
        return context

    def form_valid(self, form):
        slide_id = self.kwargs["slide_id"]
        form.instance.microscope_slide = get_object_or_404(MicroscopeSlide, id=slide_id)
        self.object = form.save()

        # Verificar se a imagem é válida
        if self.verifica_imagem_upload(self.object.image.path):
            self.classify_image(self.object)
            return super().form_valid(form)
        else:
            # Se a imagem não for válida, redirecionar para a mesma página com uma mensagem de erro
            form.add_error(None, "A imagem carregada não é válida.")
            self.object.delete()
            return self.form_invalid(form)

    def classify_image(self, slide_image):
        model = self.load_model()
        img = load_img(slide_image.image.path, target_size=(299, 299))
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        prediction = model.predict(img)
        temp = prediction
        prediction = (prediction > 0.5).astype(np.uint8)
        if prediction[0] == 1:
            slide_image.prediction_class = "Positivo"
            slide_image.prediction_percentage = round(temp[0][0] * 100, 2)
        else:
            slide_image.prediction_class = "Negativo"
            slide_image.prediction_percentage = round((1 - temp[0][0]) * 100, 2)
        slide_image.save()

    def load_model(self):
        json_path = os.path.join(
            settings.BASE_DIR, "models-classification/inception_v3.json"
        )
        model_path = os.path.join(
            settings.BASE_DIR, "models-classification/inception_v3.h5"
        )
        with open(json_path, "r") as json_file:
            saved_model_json = json_file.read()
        model = model_from_json(saved_model_json)
        model.load_weights(model_path)
        return model

    def verifica_imagem_upload(self, image_path):
        return True
        model_path = os.path.join(
            settings.BASE_DIR, "models-classification/random_forest_model.joblib"
        )

        loaded_model = joblib.load(model_path)
        return verify_image_upload(image_path, loaded_model)

    def get_success_url(self):
        return reverse(
            "list_microscope_image", kwargs={"slide_id": self.kwargs["slide_id"]}
        )


class SlideClassificationView(View):
    def get(self, request, slide_id):
        slide = MicroscopeSlide.objects.get(id=slide_id)
        images = slide.images.all()
        return render(
            request, "add_image_form.html", {"slide": slide, "images": images}
        )


class HomeView(View):
    def get(self, request):
        return render(request, "microscope_slide/home.html")
