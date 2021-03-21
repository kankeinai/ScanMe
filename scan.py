# import the necessary packages
from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils
import sys
import os
import img2pdf


def scan_photos(user_name, file_name, height, my_dir="data"):
    my_images = []
    err = []
    if not os.path.exists("scanned"):
        os.makedirs("scanned")
    for pictures in os.listdir(my_dir):
        if pictures.split('_')[0] == user_name:
            way = my_dir + "/" + pictures
            image = cv2.imread(way)
            ratio = image.shape[0] / height
            orig = image.copy()
            image = imutils.resize(image, height=height)
            # convert the image to grayscale, blur it, and find edges
            # in the image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(gray, 75, 200)
            # show the original image and the edge detected image
            # find the contours in the edged image, keeping only the
            # largest ones, and initialize the screen contour
            cnts = cv2.findContours(
                edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
            # loop over the contours
            try:
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

                # apply the four point transform to obtain a top-down
                # view of the original image
                warped = four_point_transform(
                    orig, screenCnt.reshape(4, 2) * ratio)
                # convert the warped image to grayscale, then threshold it
                # to give it that 'black and white' paper effect
                warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                T = threshold_local(warped, 15, offset=15, method="gaussian")
                warped = (warped > T).astype("uint8") * 255
                new_way = "scanned/" + "scanned_" + pictures
                cv2.imwrite(new_way, imutils.resize(warped, height=height))
                my_images.append(new_way)
            except:
                err.append(pictures)

    try:
        with open(file_name, "wb") as f:
            f.write(img2pdf.convert(my_images))
    except:
        print("something went wrong")
    for image in my_images:
        os.remove(image)

    for pictures in os.listdir(my_dir):
        way = my_dir + "/" + pictures
        if pictures.split('_')[0] == user_name:
            os.remove(way)
    return len(err) != 0
