import streamlit as st
from PIL import Image


# https://blog.loginradius.com/engineering/guest-post/opencv-web-app-with-streamlit/


def load_image(image_file):
    img = Image.open(image_file)
    return img


def main_loop():

    st.title('Simular - Edição de Imagens')
    # st.header("Simular edições de imagens")

    st.subheader("Imagem")

    chk_exibir_original = st.sidebar.checkbox('Exibir Imagem Original')

    image_file = st.file_uploader(
        "Carregar Imagem", type=["png", "jpg", "jpeg"])
    if not image_file:
        return None

    original_image = load_image(image_file)

    if chk_exibir_original:
        st.text("Original")
        st.image([original_image])


if __name__ == '__main__':
    main_loop()
