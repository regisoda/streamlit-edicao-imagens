import os
import cv2


def write_frame(img, contours=None, rect=None):
    if not record:
        return
    global frame
    frame += 1
    frameType = ""
    if contours:
        # print('contours', contours)
        frameType = "C"
        img = img.copy()
        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    if rect:
        # print('rect', rect)
        frameType = "R"
        img = img.copy()
        cv2.rectangle(img, (rect[0], rect[1]),
                      (rect[2], rect[3]), (255, 255, 0), 3)
        print("rect", rect)
    cv2.imwrite(
        'frames/frame_{:02d}_{}.png'.format(frame, frameType), img)


def get_size(img):
    """Return the size of the image in pixels."""
    ih, iw = img.shape[:2]
    return iw * ih


def white_percent(img):
    """Return the percentage of the thresholded image that's white."""
    return cv2.countNonZero(img) / get_size(img)


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


def get_contours(img):
    """Threshold the image and get contours."""
    # First make the image 1-bit and get contours
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the right threshold level
    tl = 100
    ret, thresh = cv2.threshold(imgray, tl, 255, 0)
    # print('thresh', thresh)
    print("Frame A", frame)
    write_frame(thresh)
    while white_percent(thresh) > 0.85:
        tl += 10
        ret, thresh = cv2.threshold(imgray, tl, 255, 0)
        write_frame(thresh)

    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    print("Frame B", frame)
    write_frame(img, contours=contours)

    # filter contours that are too large or small
    contours = [cc for cc in contours if contourOK(img, cc)]
    print("Frame C", frame)
    write_frame(img, contours=contours)
    print("Last Frame", frame)
    return contours


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

    print("get_boundaries", frame, minx, miny, maxx, maxy)
    write_frame(img, rect=(minx, miny, maxx, maxy))

    return (minx, miny, maxx, maxy)


def crop(img, boundaries, space=20):
    """Crop the image to the given boundaries."""
    minx, miny, maxx, maxy = boundaries
    if (maxx == 0 or maxy == 0):
        print("not crop - original")
        return img

    print("crop", minx, miny, maxx, maxy)
    return img[miny-space:maxy+space, minx-space:maxx+space]


def autocrop_image(img, record_process=False):
    global record
    global frame

    record = record_process
    frame = 0

    if record:
        os.makedirs('frames', exist_ok=True)
        dir = 'frames'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    write_frame(img)

    contours = get_contours(img)
    bounds = get_boundaries(img, contours)
    cropped = crop(img, bounds)
    if get_size(cropped) < 10000:
        print("resulting image too small, skipping output", get_size(cropped))
        return  # too small

    return cropped
