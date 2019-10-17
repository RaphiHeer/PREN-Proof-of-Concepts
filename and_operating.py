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

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# threshold the image by setting all pixel values less than 225
# to 255 (white; foreground) and all pixel values >= 225 to 255
# (black; background), thereby segmenting the image
kernel = np.ones((10,10), np.uint8)

edged_image = cv2.Canny(image, 230, 255)
edged_image = cv2.dilate(edged_image, kernel)
cv2.imshow("Edged Image", edged_image)

thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)[1]

close_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imshow("Closed Image", close_image)

and_image = cv2.bitwise_and(close_image, edged_image)
close_again = cv2.morphologyEx(and_image, cv2.MORPH_CLOSE, kernel)

cv2.imshow("And Image", close_again)

# Save images
#cv2.imwrite("docu_pictures/thresh_img.png", thresh)
#cv2.imwrite("docu_pictures/thresh_close_img.png", close_img)

cv2.waitKey(0)