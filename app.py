import streamlit as st
from PIL import Image
import cv2
import numpy as np
from rotate import auto_rotate
from extreme_points import extreme_points
from crop import autocrop_image
from external_contours import external_contours
from rectangle import external_rectangle

# https://blog.loginradius.com/engineering/guest-post/opencv-web-app-with-streamlit/


def load_image(image_file):
    img = Image.open(image_file)
    return img


def main_loop():

    st.title('Tratamento de Imagens')

    # st.header("Simular edições de imagens")
    # st.subheader("Imagem")

    st.sidebar.text("Opções:")
    chk_original_image = st.sidebar.checkbox('Exibir Imagem Original')
    chk_auto_rotate = st.sidebar.checkbox('Auto-rotação')
    chk_extreme_points = st.sidebar.checkbox('Pontos Extremos')
    chk_auto_crop = st.sidebar.checkbox('Auto-recorte')
    chk_external_rectangle = st.sidebar.checkbox('Retângulo Externo')
    chk_external_contour = st.sidebar.checkbox('Contornos Externos')

    image_file = st.file_uploader(
        "Carregar Imagem", type=["png", "jpg", "jpeg"])
    if not image_file:
        return None

    original_image = load_image(image_file)
    original_image = np.array(original_image)

    if chk_original_image:
        st.subheader("Imagem Original")
        st.image([original_image])

    st.subheader("Imagem Processada")
    processed_image = original_image

    processing_count = 0

    if chk_auto_rotate:
        processing_count += 1
        processed_image, angle = auto_rotate(processed_image, False)
        st.text(f"{processing_count}) Auto-rotação - ângulo: {angle:.04f}")

    if chk_extreme_points:
        processing_count += 1
        st.text(f"{processing_count}) Pontos extremos")
        processed_image = extreme_points(processed_image)

    if chk_auto_crop:
        processing_count += 1
        st.text(f"{processing_count}) Auto-recorte")
        processed_image = autocrop_image(processed_image, True)

    if chk_external_rectangle:
        processing_count += 1
        st.text(f"{processing_count}) Retângulo Externo")
        processed_image = external_rectangle(processed_image)

    if chk_external_contour:
        processing_count += 1
        st.text(f"{processing_count}) Contorno Externo")
        processed_image = external_contours(processed_image)

    st.image([processed_image])


if __name__ == '__main__':
    main_loop()
