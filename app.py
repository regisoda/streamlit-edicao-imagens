import streamlit as st
from PIL import Image
from rotate import auto_rotate
import cv2
import numpy as np

# https://blog.loginradius.com/engineering/guest-post/opencv-web-app-with-streamlit/


def load_image(image_file):
    img = Image.open(image_file)
    return img


def main_loop():

    st.title('Simular - Edição de Imagens')

    # st.header("Simular edições de imagens")
    # st.subheader("Imagem")

    st.sidebar.text("Opções:")
    chk_original_image = st.sidebar.checkbox('Exibir Imagem Original')

    image_file = st.file_uploader(
        "Carregar Imagem", type=["png", "jpg", "jpeg"])
    if not image_file:
        return None

    original_image = load_image(image_file)
    original_image = np.array(original_image)

    # image = cv2.imread(image_file)

    # gray_scale = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
    # st.image(gray_scale, width=300)

    if chk_original_image:
        st.text("Original")
        st.image([original_image])

    processed_image, angle = auto_rotate(original_image)
    st.text("Processada")
    st.text(f"Angulo: {angle:.04f}")
    st.image([processed_image])


if __name__ == '__main__':
    main_loop()
