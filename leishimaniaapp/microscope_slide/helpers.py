import os

import cv2
import numpy as np
import skimage


def calculate_glcm_features(image):
    # Converta a imagem para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calcule a matriz GLCM
    glcm = skimage.feature.graycomatrix(
        gray_image, distances=[1], angles=[0], levels=256, symmetric=True, normed=True
    )

    # Calcule as propriedades da matriz GLCM
    contrast = skimage.feature.graycoprops(glcm, "contrast")
    dissimilarity = skimage.feature.graycoprops(glcm, "dissimilarity")
    homogeneity = skimage.feature.graycoprops(glcm, "homogeneity")
    energy = skimage.feature.graycoprops(glcm, "energy")
    correlation = skimage.feature.graycoprops(glcm, "correlation")

    return contrast, dissimilarity, homogeneity, energy, correlation


def verify_image_upload(image_path, model):
    image = cv2.imread(image_path)
    features = calculate_glcm_features(
        image
    )  # Extrai as características GLCM da imagem
    features = np.reshape(features, (1, -1))  # Redimensiona as características
    prediction = model.predict(features)  # Faz a predição usando o modelo treinado
    print("Predição Ramdom Forest: ", prediction)

    # Classificar com base no limiar
    if prediction >= 0.5:  # limiar
        return True
    else:
        print(f"A imagem [{image_path}] não é uma imagem de microscopia.")
        os.remove(image_path)  # remove a imagem da pasta
        return False
