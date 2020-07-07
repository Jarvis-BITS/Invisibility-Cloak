import sys
import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

# Delaying system for 2 secs before webcam starts
time.sleep(2)

# Taking multiple frames to reduce noise for a good quality image.
for i in range(40):
    # Capturing just the background setting without the cloak
    ret, scene = cap.read()

    if ret is not True:
        sys.exit("Could not read the image.")

while(True):
    ret, img = cap.read()

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Detecting blue color
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv_img, lower_blue, upper_blue)

    # Segmenting out the blue color
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask1 = cv2.bitwise_not(mask)

    res1 = cv2.bitwise_and(img, img, mask=mask1)
    res2 = cv2.bitwise_and(scene, scene, mask=mask)

    # Generating the final output
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("Invisible!", final_output)

    if cv2.waitKey(1) == 27:  # esc Key
        break

cap.release()
cv2.destroyAllWindows()