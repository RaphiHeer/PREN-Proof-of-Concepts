import cv2
import imutils
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image, height = 600)
cv2.imshow("Image", image)


edged = cv2.Canny(image, 200, 255)
cv2.imshow("Edged", edged)
#cv2.imwrite("docu_pictures/canny.png", edged) # For documentation reasons
cv2.waitKey(0)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
output = image.copy()
    
# loop over the contours
for c in cnts:
    # draw each contour on the output image with a 3px thick purple
    # outline, then display the output contours one at a time
    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
    #cv2.imshow("Contours", output)

cv2.imshow("Contured image", output)

erode = cv2.erode(edged, None)
cv2.imshow("Erode", erode)

dil = cv2.dilate(edged, None)
cv2.imshow("Dil", dil)
cv2.waitKey(0)
