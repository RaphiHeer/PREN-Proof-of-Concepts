import cv2
import imutils
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image, height = 600)
cv2.imshow("Image", image)

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)

cv2.imshow("S value", s)
cv2.imshow("V value", v)

ret, s_thresh = cv2.threshold(s.copy(), 80, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("S threshold", s_thresh)

ret, v_thresh = cv2.threshold(v.copy(), 80, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("V threshold", v_thresh)

sv_combined = cv2.bitwise_and(s_thresh, v_thresh)
cv2.imshow("SV combined", sv_combined)

image_canny = cv2.Canny(image_gray, 30, 200)
cv2.imshow("Canny", image_canny)

masked_image = cv2.bitwise_and(image_gray, sv_combined)
#masked_image = cv2.bitwise_and(image, cv2.cvtColor(sv_combined, cv2.COLOR_GRAY2BGR))
cv2.imshow("Masked image", masked_image)

ret, masked_thresh = cv2.threshold(masked_image, 5, 255, cv2.THRESH_BINARY)
cv2.imshow("Masked thresh image", masked_thresh)

morph_image = cv2.morphologyEx(masked_thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_CROSS, (10,10)))
cv2.imshow("Morph image", morph_image)

experimental = cv2.bitwise_and(image_canny, morph_image)
cv2.imshow("Experimantal", experimental)

cv2.waitKey()