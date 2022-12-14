import numpy as np
import cv2
import os


def write_frame(img, aditional="", contours=None, rect=None):
    if not record:
        return

    global frame
    frame += 1
    if contours:
        img = img.copy()
        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    if rect:
        img = img.copy()
        cv2.rectangle(img, (rect[0], rect[1]),
                      (rect[2], rect[3]), (0, 255, 0), 10)
        # cv2.rectangle(img, (rect[0], rect[1]),
        #               (rect[2], rect[3]), (255, 255, 0), 3)

    cv2.imwrite('frames/frame_{:02d}{}.png'.format(frame, aditional), img)
    return img


def get_size(img):
    """Return the size of the image in pixels."""
    ih, iw = img.shape[:2]
    # print("Size", ih, iw, iw * ih)
    return iw * ih


def near_edge(img, contour, mm=0):
    """Check if a contour is near the edge in the given image."""
    x, y, w, h = cv2.boundingRect(contour)
    ih, iw = img.shape[:2]
    # mm = 10  # margin in pixels
    print('margin', mm)
    return (x < mm
            or x + w > iw - mm
            or y < mm
            or y + h > ih - mm)


def contourOK(img, cc, mm):
    """Check if the contour is a good predictor of photo location."""
    if near_edge(img, cc, mm):
        return False  # shouldn't be near edges
    x, y, w, h = cv2.boundingRect(cc)

    # if w < 100 or h < 100:
    #     return False  # too narrow or wide is bad

    area = cv2.contourArea(cc)
    # if area > (get_size(img) * 0.3):
    #     return False
    # if area < 200:
    #     return False

    if area > (get_size(img) * 0.9):
        return False

    return True


def get_boundaries(img, contours):
    """Find the boundaries of the photo in the image using contours."""
    # margin is the minimum distance from the edges of the image, as a fraction
    ih, iw = img.shape[:2]
    minx = iw
    miny = ih
    maxx = 0
    maxy = 0

    for cc in contours:
        x, y, w, h = cv2.boundingRect(cc)
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        if x + w > maxx:
            maxx = x + w
        if y + h > maxy:
            maxy = y + h

    # print("get_boundaries", frame, minx, miny, maxx, maxy)
    # rect = (minx, miny, maxx, maxy),
    img1 = write_frame(img, '_boundaries_minx{}_miny{}_maxx{}_maxy{}'.format(
        minx, miny, maxx, maxy), rect=(minx, miny, maxx, maxy))

    # return (minx, miny, maxx, maxy)
    return img1


def auto_adjust(img, use_threshold=True, threshold=200, near_margin=0, record_process=True):

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

    # apply COLOR_BGR2GRAY
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    write_frame(gray, '_gray')

    # gray = cv2.bitwise_not(gray)
    # thresh = cv2.threshold(
    #     gray, threshold, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # apply threshold
    if use_threshold:
        thresh = cv2.threshold(gray, threshold, 255, 0)[1]
        write_frame(thresh, '_tresh_{:02d}'.format(threshold))
    else:
        thresh = img

    # apply canny
    edges = cv2.Canny(thresh, 150, 200)
    write_frame(edges, '_edges')

    # find contours
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    write_frame(img, '_contours', contours=contours)

    # filter contours that are too large or small
    contours = [cc for cc in contours if contourOK(img, cc, near_margin)]
    write_frame(img, '_filterContours', contours=contours)

    bounds = get_boundaries(img, contours)

    write_frame(bounds, '_final')

    return bounds
