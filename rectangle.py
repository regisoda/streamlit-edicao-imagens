import cv2


def external_rectangle(img):
    height, width, channels = img.shape

    start_point = (0, 0)
    end_point = (width, height)
    color = (0, 0, 255)
    thickness = 10

    cv2.rectangle(img, start_point, end_point, color, thickness)

    return img
