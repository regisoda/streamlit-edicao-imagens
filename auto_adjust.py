import numpy as np
import cv2
import os


def write_frame(img, aditional="", contours=None):
    if not record:
        return

    global frame
    frame += 1
    if contours:
        # print('contours', contours)
        img = img.copy()
        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    cv2.imwrite('frames/frame_{:02d}{}.png'.format(frame, aditional), img)


def get_size(img):
    """Return the size of the image in pixels."""
    ih, iw = img.shape[:2]
    return iw * ih


def near_edge(img, contour):
    """Check if a contour is near the edge in the given image."""
    x, y, w, h = cv2.boundingRect(contour)
    ih, iw = img.shape[:2]
    mm = 2  # margin in pixels
    return (x < mm
            or x + w > iw - mm
            or y < mm
            or y + h > ih - mm)


def contourOK(img, cc):
    """Check if the contour is a good predictor of photo location."""
    if near_edge(img, cc):
        # print("near_edge")
        return False  # shouldn't be near edges
    x, y, w, h = cv2.boundingRect(cc)
    if w < 100 or h < 100:
        # print("too narrow", w, h)
        return False  # too narrow or wide is bad
    area = cv2.contourArea(cc)
    if area > (get_size(img) * 0.3):
        return False
    if area < 200:
        return False
    return True


def auto_adjust(img, use_threshold=True, threshold=200, record_process=True):

    global record
    global frame

    record = record_process
    frame = 0

    if record:
        os.makedirs('frames', exist_ok=True)
        dir = 'frames'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    write_frame(img, '_original')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.bitwise_not(gray)
    # thresh = cv2.threshold(
    #     gray, threshold, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    if use_threshold:
        thresh = cv2.threshold(gray, threshold, 255, 0)[1]
        write_frame(thresh, '_tresh_{:02d}'.format(threshold))
    else:
        thresh = img
    # contours, hierarchy = cv2.findContours(thresh, 1, 2)

    edges = cv2.Canny(thresh, 150, 200)
    write_frame(edges, '_edges')
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    write_frame(img, '_contours', contours=contours)

    # filter contours that are too large or small
    # contours = [cc for cc in contours if contourOK(img, cc)]
    # write_frame(img, '_filterContours', contours=contours)

    return thresh
