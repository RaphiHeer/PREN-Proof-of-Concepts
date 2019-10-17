from imutils.video import VideoStream
import cv2
import imutils
import time

vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    startOfPictureReading = time.time()

    # Read picture
    image = vs.read()
    image = imutils.resize(image, height = 600)
    cv2.imshow("Image", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edged_image = cv2.Canny(image, 190, 255)
    cv2.imshow("Edge", edged_image)

    cnts = cv2.findContours(edged_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    output = image.copy()
    
    # loop over the contours
    for c in cnts:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        
        # Sort out small and big contours
        if w > 400 or h > 400: continue
        if w < 50 or h < 50: continue

        # Sort out contours, which have a high difference between height and width
        heigthWidthRatio = h/w
        if (heigthWidthRatio < 0.8) | (heigthWidthRatio > 1.2): continue

        cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
        cv2.rectangle(output, (x,y), (x+w, y+h), (0,255,0), 2)


    endOfImageProcessing = time.time()

    print("Total time: %.2f" % (endOfImageProcessing - startOfPictureReading))

    cv2.imshow("Contours", output)


    
	# if q is pressed, break the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
       break