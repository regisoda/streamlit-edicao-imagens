import imutils
import cv2


def extreme_points(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # find contours in thresholded image, then grab the largest one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    # blur = cv2.GaussianBlur(gray, (3, 3), 0)
    # thresh = cv2.threshold(blur, 220, 255, cv2.THRESH_BINARY_INV)[1]
    # cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # c = max(cnts, key=cv2.contourArea)

    # determine the most extreme points along the contour
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    cv2.drawContours(image, [c], -1, (0, 255, 255), 2)

    cv2.circle(image, extLeft, 30, (255, 0, 0), -1)
    cv2.circle(image, extRight, 30, (255, 0, 0), -1)
    cv2.circle(image, extTop, 30, (255, 0, 0), -1)
    cv2.circle(image, extBot, 30, (255, 0, 0), -1)

    print('left: {}'.format(extLeft))
    print('right: {}'.format(extRight))
    print('top: {}'.format(extTop))
    print('bot: {}'.format(extBot))

    return image
