import cv2
import imutils
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-t", "--template", required=True, help="template to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
template = cv2.imread(args["template"])
(tH, tW) = template.shape[:2]

image = imutils.resize(image, height = 900)

edged_image = cv2.Canny(image, 230, 255)
edged_template = cv2.Canny(template, 230, 255)


result = cv2.matchTemplate(edged_image, edged_template, cv2.TM_CCOEFF)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
start = maxLoc
end = (start[0] + tW, start[1] + tH)
(endX, endY) = (int((maxLoc[0] + tW)), int((maxLoc[1] + tH)))

# draw a bounding box around the detected result and display the image
cv2.rectangle(image, start, end, (0, 0, 255), 2)

#cv2.imwrite("docu_pictures/tm_2.png", image)

cv2.imshow("Image", image)
cv2.imshow("Edged Image", edged_image)
cv2.imshow("Edged Template", edged_template)
cv2.waitKey(0)
