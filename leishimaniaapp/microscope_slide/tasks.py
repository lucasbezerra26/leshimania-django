from celery import shared_task
from .models import MicroscopeImage
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import model_from_json
from tensorflow.keras.applications.inception_v3 import preprocess_input
from django.conf import settings
import os
import numpy as np


@shared_task
def process_image(image_id):
    slide_image = MicroscopeImage.objects.get(id=image_id)
    model = load_model()
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


def load_model():
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
