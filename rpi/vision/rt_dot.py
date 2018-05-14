from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

res = (1280, 960)
g_rad = 11
display_frac = 1
roi_dim = 100
win_size = int(roi_dim / 2)
roi_ctd = (0, 0)

cam = PiCamera()
cam.rotation = 90
cam.framerate = 30
cam.resolution = res
raw_cam = PiRGBArray(cam, size=res)

time.sleep(0.1)

for frame in cam.capture_continuous(raw_cam, format="bgr", use_video_port=True):
    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Perform gaussian blur
    gray = cv2.GaussianBlur(gray, (g_rad, g_rad), 4)
    # Find maximum value pixel location and values (and output)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # Form a rectangular ROI of 100 x 100 pxs around max point
    img_roi = gray[maxLoc[1] - win_size:maxLoc[1] + win_size, maxLoc[0] - win_size:maxLoc[0] + win_size]
    # Find moments of inertia in ROI
    mmts = cv2.moments(img_roi)
    # Calculate centroids, store in global frame of reference and print out
    try:
        cx = int(mmts['m10'] / mmts['m00'])
        cy = int(mmts['m01'] / mmts['m00'])
        cv2.circle(img_roi, (cx, cy), 3, (0, 0, 0), -1)
        roi_ctd = (cx + maxLoc[0] - win_size, cy + maxLoc[1] - win_size)
    # If there is no data in the ROI, m00 would be null and a Zero Division error occurs
    except ZeroDivisionError:
        print("No centroid found, m00 is null")

    cv2.circle(img, roi_ctd, 3, (0, 0, 255), -1)
    cv2.circle(img, maxLoc, 1, (255, 0, 0), -1)
    cv2.rectangle(img, (maxLoc[0] - win_size, maxLoc[1] - win_size), (maxLoc[0] + win_size, maxLoc[1] + win_size),
                  (0, 255, 0), 1)
    # Show ROI and resized image
    if display_frac != 1:
        cv2.imshow("image", cv2.resize(img, (int(img.shape[1] / display_frac), int(img.shape[0] / display_frac))))
    else:
        cv2.imshow("image", img)
    cv2.imshow("roi", img_roi)
    print(roi_ctd)
    key = cv2.waitKey(1) & 0xFF
    raw_cam.truncate(0)
    if key == ord("q"):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()