from imutils.video import VideoStream
import cv2
import imutils
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True, help="template to the input image")
ap.add_argument("-p", "--picamera", required=False, type=int, default=0,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

if args["picamera"] == 1:
    vs = VideoStream(usePiCamera=True, resolution=[600, 600]).start()
else:
    vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

highestVal = 0
bestImg = None

template = cv2.imread(args["template"])
(tH, tW) = template.shape[:2]
edged_template = cv2.Canny(template, 230, 255)

while True:

    image = vs.read()

    edged_image = cv2.Canny(image, 200, 255)

    # Get width and height of template
    (tH, tW) = template.shape[:2]

    # Execute template matching over an image
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF)

    # Get worst and best matching locations
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

    # Draw bounding box over best matching location
    start = maxLoc
    end = (start[0] + tW, start[1] + tH)
    (endX, endY) = (int((maxLoc[0] + tW)), int((maxLoc[1] + tH)))
    cv2.rectangle(image, start, end, (0, 0, 255), 2)

    # draw a bounding box around the detected result and display the image
    if(maxVal > 2038356.25):

    cv2.imshow("Image", image)
    cv2.imshow("Edged Image", edged_image)
    cv2.imshow("Edged Template", edged_template)
    print(maxVal)
    print(maxLoc)

    if highestVal < maxVal:
        highestVal = maxVal
        bestImg = image.copy()
        bestEdge = edged_image.copy()
    
	# if q is pressed, break the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
       break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

cv2.imshow("Best Image Ever", bestImg)
cv2.imshow("Best Edge Ever", bestEdge)
print("Highest Value:")
print(highestVal)
cv2.waitKey(0)