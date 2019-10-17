from imutils.video import VideoStream
import cv2
import imutils
import time

vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    image = vs.read()
    image = imutils.resize(image, height = 600)
    cv2.imshow("Image", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # threshold the image by setting all pixel values less than 225
    # to 255 (white; foreground) and all pixel values >= 225 to 255
    # (black; background), thereby segmenting the image
    edged_image = cv2.Canny(image, 190, 255)
    cv2.imshow("Edge", edged_image)

    thresh = cv2.threshold(edged_image, 200, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Thresh", thresh)
    # find contours (i.e., outlines) of the foreground objects in the
    # thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    output = image.copy()
    
    # loop over the contours
    for c in cnts:
        # draw each contour on the output image with a 3px thick purple
        # outline, then display the output contours one at a time

        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        
        # Sort out small elements
        if w < 50 or h < 50: continue

        # Sort out contours, which have a high difference between height and width
        heigthWidthRatio = h/w
        if (heigthWidthRatio < 0.8) | (heigthWidthRatio > 1.2): continue


        print(cv2.contourArea(c))

        cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
        cv2.rectangle(output, (x,y), (x+w, y+h), (0,255,0), 2)


    cv2.imshow("Contours", output)


    
	# if q is pressed, break the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
       break