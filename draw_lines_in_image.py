import cv2
import imutils.video as VideoStream
import numpy as np
import math

m_info_top = 0.42 # y2 - y1 / 250
c_info_top = 50

m_info_bottom = 0.06 # 180 - 165 / 250 - 0
c_info_bottom = 165

m_stop_top = -0.52 # 190 - y1 / 250
c_stop_top = 320

m_stop_bottom = -1.1 # 200 - y1 / 250
c_stop_bottom = 490

m_info_top = 0.42  # y2 - y1 / 250
c_info_top = -20
m_info_bottom = 0.06  # 180 - 165 / 250 - 0
c_info_bottom = 175
m_stop_top = -0.52  # 190 - y1 / 250
c_stop_top = 310
m_stop_bottom = -1.1  # 200 - y1 / 250
c_stop_bottom = 330

image = cv2.imread("perfect_camera_images/linien_alle_bilder.png")
for x in np.linspace(1, 550, 10):
    cv2.drawMarker(image, (int(x), int((x*m_info_top + c_info_top))), (0,255,0))
    #cv2.drawMarker(image, (int(x), int((x*m_info_bottom + c_info_bottom))), (0,255,0))
    #cv2.drawMarke
    # r(image, (int(x), int((x*m_stop_top + c_stop_top))), (0,255,0))
    y = -0.01 * math.log(x, 0.001) + c_stop_bottom #x*m_stop_bottom + c_stop_bottom
    cv2.drawMarker(image, (int(x), int(y)), (0,255,0))
# cv2.line(image, (0, 50), (250,155), (0, 0, 255))
cv2.imshow("Image", image)
cv2.waitKey()