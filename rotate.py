import numpy as np
import cv2
import math
from os.path import basename
from scipy import ndimage


def auto_rotate(img, draw_lines=False):

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0,
                            100, minLineLength=100, maxLineGap=5)

    angles = []
    for [[x1, y1, x2, y2]] in lines:

        if (draw_lines):
            # DRAW LINES DETECTED
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    median_angle = np.median(angles)
    # print(f"Angle is {median_angle:.04f}")
    img_rotated = ndimage.rotate(img, median_angle)

    return (img_rotated, median_angle)
