from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import MicroscopeImageSerializer

import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.inception_v3 import preprocess_input


json_path = "models-classification/inception_v3.json"
model_path = "models-classification/inception_v3.h5"


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = MicroscopeImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # instance = serializer.instance
            # img = self.read_image(instance.image.path)
            #
            # with open(json_path, "r") as json_file:
            #     json_modelo_salvo = json_file.read()
            # model = model_from_json(json_modelo_salvo)
            # model.load_weights(model_path)
            #
            # prediction = model.predict(img)  # Predição
            # temp = prediction
            # prediction = (prediction > 0.5).astype(np.uint8)
            # if prediction[[0]] == 1:
            #     instance.prediction_class = "Positiva"
            #     instance.prediction_percentage = round(temp[0][0] * 100, 2)
            # else:
            #     instance.prediction_class = "Negativa"
            #     instance.prediction_percentage = round((1 - temp[0][0]) * 100, 2)
            # instance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def read_image(self, path):
        img = load_img(path, target_size=(299, 299))
        img = img_to_array(img)  # array numpy
        img = np.expand_dims(img, axis=0)  # formato de um tensor
        img = preprocess_input(img)  # entradas no padrão da rede
        return img
