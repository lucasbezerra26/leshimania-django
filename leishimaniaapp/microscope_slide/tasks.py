import os

import cv2
import numpy as np
from celery import shared_task
from django.conf import settings
from skimage.io import imread
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from ultralytics import YOLO

from .models import MicroscopeImage


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


class ImagePatcher:
    def __init__(self, path_image):
        self.path_image = path_image
        # Lê a imagem (em RGB) via skimage
        self.image = imread(self.path_image)
        self.patches = []

    def get_patches(self, patch_h=270, patch_w=480):
        """Redimensiona e divide em patches."""
        H, W, _ = self.image.shape

        # Calcula altura e largura múltiplos exatos do patch
        newH = (H // patch_h) * patch_h
        newW = (W // patch_w) * patch_w

        # Redimensiona se necessário
        if newH != H or newW != W:
            # cv2 usa (largura, altura) no resize
            self.image = cv2.resize(
                self.image, (newW, newH), interpolation=cv2.INTER_AREA
            )

        # Recalcula forma após resize
        H, W, _ = self.image.shape

        n_rows = H // patch_h
        n_cols = W // patch_w
        self.patches = []

        for row in range(n_rows):
            row_patches = []
            for col in range(n_cols):
                x_init = row * patch_h
                x_end = (row + 1) * patch_h
                y_init = col * patch_w
                y_end = (col + 1) * patch_w

                # Recorta o patch
                patch = self.image[x_init:x_end, y_init:y_end, :]
                row_patches.append(patch)
            self.patches.append(row_patches)

        return self.patches


@shared_task
def process_image_yolo(image_id):
    slide_image = MicroscopeImage.objects.get(id=image_id)

    # 1) Pega os patches (como no seu código)
    patcher = ImagePatcher(slide_image.image.path)
    patches_matrix = patcher.get_patches(patch_h=270, patch_w=480)

    # 2) Carrega modelo YOLO
    model = YOLO("models-classification/yolo.pt")

    # Variável para somar bounding boxes
    total_boxes = 0

    annotated_patches_matrix = []
    for row_patches in patches_matrix:
        annotated_row = []
        for patch in row_patches:
            results = model.predict(patch, conf=0.25)
            annotated_patch = patch.copy()

            # Contar quantas bounding boxes foram retornadas
            num_boxes = len(results[0].boxes.xyxy)
            total_boxes += num_boxes

            for box in results[0].boxes.xyxy:
                x_min, y_min, x_max, y_max = box
                cv2.rectangle(
                    annotated_patch,
                    (int(x_min), int(y_min)),
                    (int(x_max), int(y_max)),
                    (0, 255, 0),
                    2,
                )
            annotated_row.append(annotated_patch)
        annotated_patches_matrix.append(annotated_row)

    # Reconstrução da imagem final
    linhas_concat = []
    for row_patches in annotated_patches_matrix:
        linha_completa = np.concatenate(row_patches, axis=1)
        linhas_concat.append(linha_completa)

    final_image = np.concatenate(linhas_concat, axis=0)
    final_image_rgb = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)

    annotated_path = os.path.join(
        settings.MEDIA_ROOT, f"{MicroscopeImage.PATH_RESULT}anno_{image_id}.png"
    )

    cv2.imwrite(annotated_path, final_image_rgb)
    slide_image.image_result.name = f"{MicroscopeImage.PATH_RESULT}anno_{image_id}.png"
    if total_boxes > 0:
        slide_image.prediction_class = "Positivo"
    else:
        slide_image.prediction_class = "Negativo"

    slide_image.save()

    return f"YOLO processing finished for MicroscopeImage {image_id}!"
