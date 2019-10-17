import cv2

image = cv2.imread("perfect_camera_images/gerade.png")

x = 135
y = 131
h = 30
w = 16

image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 200), 2)

# Calculate new Height
newHeight = int(h * 1.4)
heightDiffPerSite = int((newHeight - h) / 2)
leftY = y - heightDiffPerSite

# Correct width to heigth ratio to get a square
diffHW = h-w
addProSite = diffHW / 2

leftX = int(x - addProSite)
rightX = int(x + w + addProSite)

print((leftX, leftY), (rightX, leftY + newHeight))

image = cv2.rectangle(image, (leftX, leftY), (rightX, leftY + newHeight), (0, 200, 0), 2)
cv2.imshow("Image", image)
cv2.waitKey()