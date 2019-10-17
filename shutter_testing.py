# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
#from pivideostream import *
import time
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fps", default=20, required=False, help="Approx. desired FPS")
ap.add_argument("-s", "--subdir", default="default", required=False, help="Subdir to safe")
args = vars(ap.parse_args())

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()

camera.resolution = (640, 480)
camera.framerate = args['fps']
camera.exposure_mode = 'off'
camera.iso = 1600
camera.shutter_speed = 1500
camera.rotation = 180

folderPath = 'imageSeries/' + str(args['subdir']) + '/' + str(args['fps']) + '_' + str(time.time()) + '_'
imageIndex = 0

#rawCapture = PiRGBArray(camera, size=(1024, 768))
rawCapture = PiRGBArray(camera, size=(640, 480))
#vs = PiVideoStream().start()
 
# allow the camera to warmup
time.sleep(3)
 

# capture frames from the camera
#while True:
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    print("Shutter Speed")
    print(camera.shutter_speed, camera.exposure_speed)
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    #image = vs.read()

    #cv2.imshow("Image", image)
    current_shutter = camera.shutter_speed
    filename = folderPath + ("%05d" % imageIndex) + '_' +  ("%d" % current_shutter) + '.png'
    print("File Path: " + filename)

    cv2.imwrite(filename, image)
    print("Saved image number %d" % imageIndex)

    if (imageIndex % 5) == 0:
        #current_shutter -= 100

        #if current_shutter < 1000:
        #    current_shutter = 5000

        #camera.shutter_speed = current_shutter
        print(current_shutter)


    imageIndex += 1

    # show the frame
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if imageIndex > 200:
        break

print("Shutter testing finished")