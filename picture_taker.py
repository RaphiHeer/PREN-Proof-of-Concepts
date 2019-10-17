# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
#from pivideostream import *
import time
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fps", default=30, required=False, help="Approx. desired FPS")
ap.add_argument("-s", "--subdir", default="default", required=False, help="Subdir to safe")
args = vars(ap.parse_args())

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()

camera.resolution = (640, 480)
camera.framerate = args['fps']
camera.iso = 1000
camera.shutter_speed = 7000
camera.exposure_mode = 'off'
camera.rotation = 180

"""

camera.iso = 800
camera.resolution = '720p'
camera.exposure_mode = 'off'
camera.shutter_speed = 30


camera.iso = 800
camera.resolution = '720p'
camera.framerate = args['fps']
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'


camera.iso = 800
camera.resolution = '720p'
camera.framerate = args['fps']
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'


"""

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
	
	filename = folderPath + ("%05d" % imageIndex) + '.png'
	print("File Path: " + filename)
	cv2.imwrite(filename, image)
	print("Saved image number %d" % imageIndex)
	
	
	#cv2.imshow("Image", image)
	imageIndex += 1

	# show the frame
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break