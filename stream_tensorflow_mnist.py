#!/usr/bin/env python

# Copyright dhq 2018 Aug 31
# Licensed under do whatever the heck you want with it as long as Derek Zoolander agrees with it.

#Theory of operation

# 1. read image
# 2. convert to gray scale
# 3. convert to uint8 range
# 4. threshold via otsu method
# 5. resize image
# 6. invert image to balck background
# 7. Feed into trained neural network 
# 8. print answer

from skimage.io import imread
from skimage.transform import resize
import numpy as np
from skimage import data, io
from matplotlib import pyplot as plt
from skimage import img_as_ubyte		#convert float to uint8
from skimage.color import rgb2gray
import cv2
import datetime
import argparse
import imutils
import time
from time import sleep
from imutils.video import VideoStream
from keras.models import load_model

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

#import CNN model weight
model=load_model('model/mnist_trained_model.h5')

 
# initialize the video stream and allow the cammera sensor to warmup
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

last_time = time.time()

# loop over the frames from the video stream
while True:
    try:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        
        # draw the timestamp on the frame
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.35, (0, 0, 255), 1)
        
        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        

        im_gray = rgb2gray(frame)				#convert original to gray image
        #plt.show()
        img_gray_u8 = img_as_ubyte(im_gray)		# convert grey image to uint8
        cv2.imshow("Image Gray u8", img_gray_u8)
        #plt.show()
        #Convert grayscale image to binary
        (thresh, im_bw) = cv2.threshold(img_gray_u8, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imshow("Image BW", im_bw)
        #resize using opencv
        img_resized = cv2.resize(im_bw,(28,28))
        cv2.imshow("Image Resized", img_resized)

        im_resize = resize(im_bw,(28,28), mode='constant')
        io.imshow(im_resize) 

        cv2.imshow("Image Resize again", im_resize)

        im_gray_invert = 255 - img_resized
        cv2.imshow("Image Gray invert", im_gray_invert)

        im_final = im_gray_invert.reshape(1,28,28,1)

        current_time = time.time()
        print("Times passed: %f" % (current_time - last_time))
        print("Estimated FPS: %f" % (1 / (current_time - last_time)))
        last_time = current_time

    except KeyboardInterrupt:
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()

    # if the `q` key was pressed, break from the loop
	# if q is pressed, break the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
       break
            