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

# Edge detection on Image
edged_image = cv2.Canny(image, 240, 255)
cv2.imshow("Edged", edged_image)
outputEdgedImage = image.copy()

# Find contours on Image
cnts = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# loop over the contours
for c in cnts:

    # Get bounding box of contour
    rect = cv2.boundingRect(c)
    x,y,w,h = rect
    
    # Sort out contours, which have a high difference between height and width
    heigthWidthRatio = h/w
    if (heigthWidthRatio < 0.5) | (heigthWidthRatio > 1.5): continue
    
    # Sort out small elements (smaller than a certain amount of pixels)
    if (w < 30) | (h < 30): continue
    
    # Sort out big elements (bigger than a certain amount of pixels)
    if (w > 100) | (h > 100): continue

    # Draw contours on image
    cv2.drawContours(outputImage, [c], -1, (240, 0, 159), 3)

    # Draw bounding box on image
    cv2.rectangle(outputImage, (x,y), (x+w, y+h), (0,255,0), 2)


cv2.imshow("ThreshContours", outputEdgedImage)
cv2.imshow("Edged Draw", edged_draw)

# threshold the image by setting all pixel values less than 225
# to 255 (white; foreground) and all pixel values >= 225 to 255
# (black; background), thereby segmenting the image

# Thresholding on image
ret = cv2.threshold(grayImage, 245, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
threshImage = ret[1]

cv2.imshow("Thresh", thresh)

# Create kernel for morph operation
kernel = np.ones((8,8), np.uint8)

# Execute morph operation on image
close_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)


cv2.imshow("Closed image", close_img)


#cv2.imwrite("docu_pictures/image_processed.png", outputEdgedImage)
#cv2.imwrite("docu_pictures/thresh_close_img.png", close_img)

cv2.waitKey(0)