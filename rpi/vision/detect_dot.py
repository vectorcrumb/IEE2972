import cv2
import numpy as np 

g_rad = 11
display_frac = 2
roi_dim = 240
win_size = int(roi_dim / 2)
roi_ctd = (0, 0)

img_names = ["image{}.jpg".format(i) for i in range(5)]
imgs = [cv2.imread(img_name, cv2.IMREAD_COLOR) for img_name in img_names]

# Obtain first image and convert to grayscale
img = imgs[0]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Perform gaussian blur
gray = cv2.GaussianBlur(gray, (g_rad, g_rad), 4)
# Find maximum value pixel location and values (and output)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
print("minMaxLoc returned: ", minVal, maxVal, minLoc, maxLoc)
# Form a rectangular ROI of 100 x 100 pxs around max point
img_roi = gray[maxLoc[1]-win_size:maxLoc[1]+win_size, maxLoc[0]-win_size:maxLoc[0]+win_size]
# Find moments of inertia in ROI
mmts = cv2.moments(img_roi)
# Calculate centroids, store in global frame of reference and print out
try:
    cx = int(mmts['m10']/mmts['m00'])
    cy = int(mmts['m01']/mmts['m00'])
    cv2.circle(img_roi, (cx, cy), 3, (0, 0, 0), -1)
    roi_ctd = (cx + maxLoc[0] - win_size, cy + maxLoc[1] - win_size)
    print("Window centroid:", roi_ctd)
    print("Max point:", maxLoc)
# If there is no data in the ROI, m00 would be null and a Zero Division error occurs
except ZeroDivisionError:
    print("No centroid found, m00 is null")
# Create copy of image and display point, ROI
image = img.copy()
cv2.circle(image, maxLoc, 5, (255, 0, 0), -1)
cv2.circle(image, roi_ctd, 3, (0, 255, 0), -1)
cv2.rectangle(image, (maxLoc[0]-win_size, maxLoc[1]-win_size), (maxLoc[0]+win_size, maxLoc[1]+win_size), (0, 255, 0), 1)
# Show ROI and resized image
cv2.imshow('gray', img_roi)
cv2.imshow('image',cv2.resize(image, (int(image.shape[1]/display_frac), int(image.shape[0]/display_frac))))
cv2.waitKey(0)
cv2.destroyAllWindows()