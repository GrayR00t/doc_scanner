# USAGE
# python scan.py --image images/page.jpg


def scan():

    # import the necessary packages
    from transform.transform import four_point_transform
    from skimage.filters import threshold_local
    import numpy as np
    import argparse
    import cv2
    import imutils
    import os

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="Path to the image to be scanned")

    ap.add_argument("-o", "--path", required=True,
                    help="Path to output dir")
    args = vars(ap.parse_args())

    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    image = cv2.imread(args["image"])
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    '''
	 A neat performance hack that I like to do is actually sort the contours by area and keep only the largest ones.
	 This allows us to only examine the largest of the contours, discarding the rest.'''

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    # show the contour (outline) of the piece of paper
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    cv2.imshow("warped", warped)
    cv2.waitKey(3000)
    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset=10, method="gaussian")
    warped = (warped > T).astype("uint8") * 255
    img = imutils.resize(warped, height=650)
    cv2.imwrite(os.path.join(args["path"], 'output.jpg'), img)
