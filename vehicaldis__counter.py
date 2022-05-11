import cv2
import imutils
import numpy as np

# starting web camera
cap = cv2.VideoCapture('WhatsApp Video 2022-04-20 at 8.36.44 PM.mp4')

count_line_position = 500

minW = 80
minH = 80


#Initialize Substructor
algo = cv2.createBackgroundSubtractorMOG2()


def center_handle(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1

    return cx, cy


detect = []
offset = 6
count = 0

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=1050)
    grey = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 1)
    # applying on each frame
    img_sub = algo.apply(blur)
    dilate = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    counterShape, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, (25, count_line_position), (1200, count_line_position), (255, 214, 3),3)

    for (i, c) in enumerate(counterShape):
        (x, y, w, h) = cv2.boundingRect(c)
        var_counter = (w>= minW) and (h>= minH)
        if not var_counter:
            continue

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 220, 3))

        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame, center, 4, (0, 23, 233), -1)

        for (x, y) in detect:
            if y < (count_line_position+offset) and y > (count_line_position+offset):
                count = count +1

            cv2.line(frame, (25, count_line_position), (1200, count_line_position), (25, 24, 30),3)
            detect.remove((x, y))
    print("Vehicle count: ",str(count))

    cv2.putText(frame, "VEHICLE_COUNT: "+ str(count), (450,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (2, 2, 222), 5)



    cv2.imshow("Ima", dilatada)
    cv2.imshow("Image", frame)
    cv2.waitKey(1)