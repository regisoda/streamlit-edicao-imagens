import streamlit as st
from PIL import Image
import numpy as np
# from rotate import auto_rotate
# from extreme_points import extreme_points
# from crop import autocrop_image
# from external_contours import external_contours
# from rectangle import external_rectangle
# from screw_text import screw_text
from auto_adjust import auto_adjust


# https://blog.loginradius.com/engineering/guest-post/opencv-web-app-with-streamlit/


def load_image(image_file):
    img = Image.open(image_file)
    return img


def main_loop():

    # https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

    st.sidebar.text("Opções:")
    chk_original_image = st.sidebar.checkbox('Exibir Imagem Original', False)
    chk_processed_image = st.sidebar.checkbox(
        'Exibir Imagem Processada', True)
    # chk_show_rotated_image = st.sidebar.checkbox(
    #     'Exibir Parâmetros Auto-Rotação', False)

    chk_auto_adjust = True
    # chk_auto_adjust = st.sidebar.checkbox('Auto-ajuste', True)
    # chk_auto_rotate = st.sidebar.checkbox('Auto-rotação')
    # chk_auto_rotate_text = st.sidebar.checkbox('Auto-rotação Texto')
    # chk_extreme_points = st.sidebar.checkbox('Pontos Extremos')
    # chk_auto_crop = st.sidebar.checkbox('Auto-recorte')
    # chk_external_rectangle = st.sidebar.checkbox('Retângulo Externo')
    # chk_external_contour = st.sidebar.checkbox('Contornos Externos')

    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.text("Ajustes manuais:")

    chk_use_threshold = False
    threshold = 0
    near_margin_left = 0
    near_margin_top = 0
    near_margin_right = 0
    near_margin_bottom = 0

    # chk_use_threshold = st.sidebar.checkbox('Usar Threshold')
    # if (chk_use_threshold):
    #     threshold = st.sidebar.slider('Ajuste (Threshold)', 100, 250, 200)
    #     st.write("Threshold:", threshold)

    chk_auto_adjust_rotate = st.sidebar.checkbox(
        'Auto-rotação', False)
    chk_show_rotated_image = chk_auto_adjust_rotate

    chk_use_margin = st.sidebar.checkbox(
        'Configurar ruídos próximos das margens', False)
    if (chk_use_margin):
        st.sidebar.write("Desconsiderar:")
        near_margin_left = st.sidebar.slider(
            'Qtde de Pixels (Esquerda)', 0, 150, 0)
        near_margin_top = st.sidebar.slider(
            'Qtde de Pixels (Superior)', 0, 150, 0)
        near_margin_right = st.sidebar.slider(
            'Qtde de Pixels (Direita)', 0, 150, 0)
        near_margin_bottom = st.sidebar.slider(
            'Qtde de Pixels (Inferior)', 0, 150, 0)

    # ------------------------------------------ #
    # ------------------------------------------ #
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.markdown(
        ":facepunch: Desenvolvido por Régis Oda :copyright: - v0.1")

    # ------------------------------------------ #
    # ------------------------------------------ #
    st.title('Pattero - Tratamento de Imagens')
    # st.caption('v0.1')

    image_file = st.file_uploader(
        "Carregar Imagem", type=["png", "jpg", "jpeg"])
    if not image_file:
        return None

    original_image = load_image(image_file)
    original_image = np.array(original_image)

    if chk_original_image:
        st.subheader("Imagem Original")
        st.image([original_image])

    processed_image = original_image
    final_image = original_image

    processing_count = 0

    # if chk_auto_rotate:
    #     processing_count += 1
    #     processed_image, angle = auto_rotate(processed_image, False)
    #     st.text(f"{processing_count}) Auto-rotação - ângulo: {angle:.04f}")

    # if chk_auto_rotate_text:
    #     processing_count += 1
    #     processed_image, angle = screw_text(processed_image, True)
    #     st.text(f"{processing_count}) Auto-rotação - texto: {angle:.04f}")

    # if chk_extreme_points:
    #     processing_count += 1
    #     st.text(f"{processing_count}) Pontos extremos")
    #     processed_image = extreme_points(processed_image)

    # if chk_auto_crop:
    #     processing_count += 1
    #     st.text(f"{processing_count}) Auto-recorte")
    #     processed_image = autocrop_image(processed_image, True)

    # if chk_external_rectangle:
    #     processing_count += 1
    #     st.text(f"{processing_count}) Retângulo Externo")
    #     processed_image = external_rectangle(processed_image)

    # if chk_external_contour:
    #     processing_count += 1
    #     st.text(f"{processing_count}) Contorno Externo")
    #     processed_image = external_contours(processed_image)

    if chk_auto_adjust:
        processing_count += 1
        final_image, median_angle, rotated_image, processed_image = auto_adjust(
            processed_image,
            chk_use_threshold,
            threshold,
            near_margin_left,
            near_margin_top,
            near_margin_right,
            near_margin_bottom,
            auto_rotate=chk_auto_adjust_rotate,
            crop=True,
            record_process=True)
        # st.text(f"{processing_count}) Auto-ajuste")

    if chk_processed_image:
        st.subheader("Imagem Processada")
        st.image([processed_image])

    if chk_show_rotated_image:
        # st.subheader("Parâmetros Auto-Rotação")
        if median_angle != 0:
            st.text(f"Auto-rotação - ângulo: {median_angle:.04f}")
            # st.image([rotated_image], width=400)
            # st.image([rotated_image])
        else:
            st.text(f"Auto-rotação: não realizada")

    st.subheader("Resultado Final")
    st.image([final_image])


if __name__ == '__main__':
    main_loop()
