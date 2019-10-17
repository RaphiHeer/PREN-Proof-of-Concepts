from skimage.io import imread
from skimage.transform import resize
import numpy as np
from pandas import Series
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
from pivideostream import *

def printStatistics(title, statList):
    print(title)
    print("Mean: %.4f Median: %.4f Max: %.4f Min: %.4f Number of meassures: %i\n" % (np.mean(statList), np.median(statList), np.max(statList), np.min(statList), np.size(statList)))
    return

#import CNN model weight
model=load_model('model/mnist_trained_model.h5')

vs = VideoStream(src=0).start()
time.sleep(2.0)

list_time_all = np.array([])
list_contour_detection = np.array([])
list_contour_calculation = np.array([])
list_predict_all = np.array([])

start_of_application = time.time()

while True:

    start_of_all = time.time()

    image = vs.read()
    image = imutils.resize(image, height = 600)
    image = cv2.flip(image.copy(), 0)
    image = cv2.flip(image.copy(), 1)
    cv2.imshow("Image", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # threshold the image by setting all pixel values less than 225
    # to 255 (white; foreground) and all pixel values >= 225 to 255
    # (black; background), thereby segmenting the image
    edged_image = cv2.Canny(gray, 224, 255)
    cv2.imshow("Edge", edged_image)

    # find contours (i.e., outlines) of the foreground objects in the
    # thresholded image
    cnts = cv2.findContours(edged_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    output = image.copy()

    end_of_contour_detection = time.time()
    time_for_contour_detection = end_of_contour_detection - start_of_all
    list_contour_detection = np.append(list_contour_detection, time_for_contour_detection)

    start_contour_evaluation = time.time()
    # loop over the contours
    for c in cnts:
        # draw each contour on the output image with a 3px thick purple
        # outline, then display the output contours one at a time

        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        

        print(x, y, w, h)
        if x < 20 or y < 20 or ((x + w) > 500) or ((y+h) > 500):
            cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
            cv2.rectangle(output, (x,y), (x+w, y+h), (0,0,255), 2)
            continue

        # Sort out small elements
        if w < 50 or h < 50:
            cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
            cv2.rectangle(output, (x,y), (x+w, y+h), (0,0,255), 2)
            continue

        # Sort out contours, which have a high difference between height and width
        #heigthWidthRatio = h/w
        #if (heigthWidthRatio < 0.5) | (heigthWidthRatio > 1.5): 
        #    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
        #    cv2.rectangle(output, (x,y), (x+w, y+h), (0,50,210), 2)
        #    continue

        # Resize image for DNN-Prediction
        im_cutted = gray[y-5:(y+h+5),x-5:(x+w+5)].copy()

        print(x, y, w, h)
        print(im_cutted.shape)
        if im_cutted[5,5] >= 150 & im_cutted[8,8] >= 150:
            im_cutted_and_inverted = cv2.threshold(im_cutted.copy(), 100, 255, cv2.THRESH_BINARY_INV)[1]
        else:
            im_cutted_and_inverted = cv2.threshold(im_cutted.copy(), 100, 255, cv2.THRESH_BINARY)[1]
        # If something went wrong in the thresholding function: continue
        if im_cutted_and_inverted is None:
            cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
            cv2.rectangle(output, (x,y), (x+w, y+h), (0,0,255), 2)
            continue

        im_resize1 = cv2.resize(im_cutted_and_inverted, (28,28))
        im_resize2 = resize(im_resize1,(28,28), mode='constant')
        im_final = im_resize2.reshape(1,28,28,1)

        cv2.imshow("Resize", im_resize2)

        # Predict digit on image
        start_predict = time.time()
        ans = model.predict(im_final)
        time_for_predict = time.time() - start_predict

        list_predict_all = np.append(list_predict_all, time_for_predict)

        number = ans[0].tolist().index(max(ans[0].tolist()))
        prob = ans[0].tolist()[number] * 100

        if prob < 80:
            continue

        print(ans.shape)

        #cv2.waitKey()
        #print(ans[0])
        #print('DNN predicted digit is: ',ans)

        #print(cv2.contourArea(c))

        # Print predicted digit
        cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
        cv2.rectangle(output, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(output, ("%i" % number), (x-20, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(output, ("%.3f %%" % prob), (x + 50, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        summe = 0
        for i in range(0, 9):
            #print(ans[0].tolist()[i])
            summe += ans[0].tolist()[i]
        print("Sum: %.2f" % summe)

        #cv2.waitKey()

    if np.size(cnts) > 0:
        time_for_contour_evaluation = time.time() - start_contour_evaluation
        list_contour_calculation = np.append(list_contour_calculation, time_for_contour_evaluation)

    cv2.imshow("Contours", output)

    end_of_all = time.time() - start_of_all
    
    list_time_all = np.append(list_time_all, end_of_all)

    print("Mean of time: %.4f, Count of meassures: %i" % (np.mean(list_time_all), list_time_all.size))

	# if q is pressed, break the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
       break
    #time.sleep(1)

application_time = time.time() - start_of_application

print("-------------------")
print("Overall Statistics:")
print("-------------------")

number_of_pictures = np.size(list_time_all)
if(number_of_pictures > 0):
    fps = number_of_pictures / application_time
    print("FPS: %.2f; Number of pictures: %i;   Application time: %.2f\n" % (fps, number_of_pictures, application_time))


printStatistics("Statistics for contour detection", list_contour_detection)
printStatistics("Statistics for contour calculations", list_contour_calculation)
printStatistics("Statistics for number prediction:", list_predict_all)
printStatistics("Total statistic per image", list_time_all)