import numpy as np
import cv2
import os


def auto_adjust(img, threshold=200, record_process=True):

    if record_process:
        os.makedirs('frames', exist_ok=True)
        dir = 'frames'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.bitwise_not(gray)
    # thresh = cv2.threshold(
    #     gray, threshold, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = cv2.threshold(gray, threshold, 255, 0)[1]

    if record_process:
        cv2.imwrite('frames/frame_tresh_{:02d}.png'.format(threshold), thresh)

    return thresh
