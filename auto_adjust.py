import numpy as np
import math
import cv2
import os
from scipy import ndimage


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


def near_edge(img, contour,
              near_margin_left,
              near_margin_top,
              near_margin_right,
              near_margin_bottom,
              mm):
    """Check if a contour is near the edge in the given image."""
    x, y, w, h = cv2.boundingRect(contour)
    ih, iw = img.shape[:2]

    # print('NEAR', near_margin_left, near_margin_top,
    #       near_margin_right, near_margin_bottom, mm)
    # print('--', x, y, h, w)
    # print('y + h', y + h)
    # print('ih iw', ih, iw)

    if (near_margin_left > 0):
        if (x <= near_margin_left):
            print('near left', y, near_margin_left)
            return True

    if (near_margin_top > 0):
        if (y <= near_margin_top):
            print('near top', y, near_margin_top)
            return True

    if (near_margin_right > 0):
        if (x + w >= iw - near_margin_right):
            print('near right', x + w, iw - near_margin_right)
            return True

    if (near_margin_bottom > 0):
        if (y + h >= ih - near_margin_bottom):
            print('near bottom', y + h, ih - near_margin_bottom)
            return True

    return (x < mm
            or x + w > iw - mm
            or y < mm
            or y + h > ih - mm)


def contourOK(img, cc,
              near_margin_left,
              near_margin_top,
              near_margin_right,
              near_margin_bottom):
    """Check if the contour is a good predictor of photo location."""
    if near_edge(
            img,
            cc,
            near_margin_left,
            near_margin_top,
            near_margin_right,
            near_margin_bottom,
            mm=5):
        # print('near_edge')
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


def get_boundaries(img, contours, addSpaceTop=20, maxMarginHeight=40, maxMarginWidth=100):
    """Find the boundaries of the photo in the image using contours."""
    ih, iw = img.shape[:2]
    minx = iw
    miny = ih
    maxx = 0
    maxy = 0

    minHeightY = ih - maxMarginHeight
    minWidthX = iw - maxMarginWidth

    # print("ih", ih, minHeightY)
    # print("iw", iw, minWidthX)

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

    if (addSpaceTop > 0 and miny > addSpaceTop):
        miny -= addSpaceTop

    if (maxy > 0 and maxy < minHeightY):
        print("adjust maxy", maxy, minHeightY)
        maxy = minHeightY

    if (maxx > 0 and maxx < minWidthX):
        print("adjust maxx", maxx, minWidthX)
        maxx = minWidthX

    # print("get_boundaries", frame, minx, miny, maxx, maxy)
    # rect = (minx, miny, maxx, maxy),

    imgBoundary = write_frame(img, '_boundaries_minx{}_miny{}_maxx{}_maxy{}'.format(
        minx, miny, maxx, maxy), rect=(minx, miny, maxx, maxy))

    return (imgBoundary, (minx, miny, maxx, maxy))


def auto_rotate_image(img, draw_lines=True):
    write_frame(img, '_rotate_before')

    image_rotated_lines = img.copy()
    img_gray = cv2.cvtColor(image_rotated_lines, cv2.COLOR_BGR2GRAY)
    write_frame(img_gray, '_rotate_gray')
    img_edges = cv2.Canny(img_gray, 100, 200, apertureSize=3)
    # img_edges = cv2.Canny(img_gray, 150, 200)
    write_frame(img_edges, '_rotate_edges')
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100,
                            minLineLength=150, maxLineGap=5)
    angles = []
    median_angle = 0
    image_result = img

    if lines is not None:
        for [[x1, y1, x2, y2]] in lines:
            print('lines', (x1, y1), (x2, y2))
            valid_lines = (y1 - y2 >= 0 and y1 - y2 <
                           20) or (y2 - y1 >= 0 and y2 - y1 < 20)
            if (valid_lines):
                print('lines *', (x1, y1), (x2, y2))
                if (draw_lines):
                    cv2.line(image_rotated_lines, (x1, y1),
                             (x2, y2), (255, 255, 0), 20)

                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
                angles.append(angle)
            else:
                if (draw_lines):
                    cv2.line(image_rotated_lines, (x1, y1),
                             (x2, y2), (0, 255, 255), 2)

        if len(angles) > 1:
            median_angle = np.median(angles)
            print(f"Angle is {median_angle:.04f}")
        else:
            print('Angles not enough')
    else:
        print('No detected lines')

    write_frame(image_rotated_lines, '_rotate_lines')

    if median_angle != 0:
        image_result = ndimage.rotate(img, median_angle)
        write_frame(image_result, '_rotate_after')
    else:
        write_frame(image_result, '_rotate_after_no')

    return (image_result, median_angle, image_rotated_lines)


def crop_image(img, boundaries, space=0):
    """Crop the image to the given boundaries."""
    minx, miny, maxx, maxy = boundaries
    if (maxx == 0 or maxy == 0):
        print("not crop - original")
        return img

    # print("crop", minx, miny, maxx, maxy)
    return img[miny-space:maxy+space, minx-space:maxx+space]


def auto_adjust(img,
                use_threshold=True,
                threshold=200,
                near_margin_left=0,
                near_margin_top=0,
                near_margin_right=0,
                near_margin_bottom=0,
                auto_rotate=False,
                crop=True,
                record_process=True):

    global record
    global frame

    record = record_process
    frame = 0
    processed_image = img.copy()

    if record:
        os.makedirs('frames', exist_ok=True)
        dir = 'frames'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    write_frame(img, '_original')

    if auto_rotate:
        processed_image, median_angle, image_rotated_result = auto_rotate_image(
            processed_image)
    else:
        median_angle = 0
        image_rotated_result = img.copy()

    # apply COLOR_BGR2GRAY
    gray_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    write_frame(gray_image, '_gray')

    # gray = cv2.bitwise_not(gray)
    # thresh = cv2.threshold(
    #     gray, threshold, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # apply threshold
    thresh_image = processed_image
    if use_threshold:
        thresh_image = cv2.threshold(gray_image, threshold, 255, 0)[1]
        write_frame(thresh_image, '_tresh_{:02d}'.format(threshold))

    # apply canny
    edges_image = cv2.Canny(thresh_image, 150, 200)
    write_frame(edges_image, '_edges')

    # find contours
    contours, hierarchy = cv2.findContours(
        edges_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    write_frame(processed_image, '_contours', contours=contours)

    # filter contours that are too large or small
    contours = [cc for cc in contours
                if contourOK(
                    processed_image,
                    cc,
                    near_margin_left,
                    near_margin_top,
                    near_margin_right,
                    near_margin_bottom)
                ]
    write_frame(processed_image, '_filterContours', contours=contours)

    image_processed_result, bounds = get_boundaries(processed_image, contours)

    write_frame(processed_image, '_cropped_before')

    image_result = processed_image
    if crop:
        image_result = crop_image(processed_image, bounds)

    write_frame(image_result, '_cropped_after')

    # if auto_rotate:
    #     processed_image, median_angle, image_rotated_result = auto_rotate_image(
    #         image_result)
    # else:
    #     median_angle = 0
    #     image_rotated_result = image_result.copy()

    write_frame(image_result, '_final')

    return (image_result, median_angle, image_rotated_result, image_processed_result)
