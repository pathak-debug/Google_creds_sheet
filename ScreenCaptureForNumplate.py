import cv2
import imutils
import numpy as np
import pyautogui

# web camara
# cap = cv2.VideoCapture('video.mp4')
from Number_Plate_dict import extract_num

cap = cv2.VideoCapture('WhatsApp Video 2022-04-20 at 9.16.39 PM.mp4')

min_wid_rect = 80  # min width
min_hit_rect = 80  # min height

count_line_position = 900
# initialize
algo = cv2.createBackgroundSubtractorMOG2()


def center_handle(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


detect = []
offset = 6# Allowable errorcbetween pixel
counter = 0

while (True):
    ret, frame1 = cap.read()
    frame1 = imutils.resize(frame1, width = 1060)
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    # applying on each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    counterShape, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)

    for (i, c) in enumerate(counterShape):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_counter = (w >= min_wid_rect) and (h >= min_hit_rect)
        if not validate_counter:
            continue;

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText(frame1,"VEHICLE COUNTER :"+str(counter),(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)


        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)



        for (x,y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                # pyautogui.screenshot('image.png')
                result = True
                count = 0
                while(result):
                    if count < 10000:
                        count = count + 1
                    if count == 10000:
                        cv2.imwrite("image.png", frame1)
                        result = False
                extract_num('image.png')
                counter = counter + 1
                cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (0, 127, 255), 3)
                detect.remove((x,y))
                # print( " vehhical counter "+str(counter))
                exit(0)
                break

    # cv2.putText(frame1,"VEHICLE COUNTER :"+str(counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)


    # cv2.imshow('Detecter', dilatada)

    cv2.imshow('video Original', frame1)

    if cv2.waitKey(1) == 13:
        break;

cv2.destroyAllWindows();
cap.release()
