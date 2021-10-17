from os import truncate
import cv2
import time
import datetime

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
time_started = None
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size =(int(cap.get(3)), int(cap.get(4)))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

while True:

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
    # these return a list of rectangles i.e, arrays of arrays( arr[a[], a[], a[], ....]) 

    if len(faces) + len(bodies) > 0:

        if detection:
            time_started = False       
        else:
            detection = True
            curr_time = datetime.datetime.now().strftime("%d-%m-%Y-%Y-%H-%S")
            out = cv2.VideoWriter(f"{curr_time}.mp4", fourcc, 20, frame_size)
            print('Startec recording!')

    elif detection:

        if time_started:
            if time.time() - detection_stopped_time > SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                time_started = False
                out.release()
                print('Stop Recording!')
        
        else:
            time_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    # for (x, y, width, height) in faces:
    #     cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 5)      

    cv2.imshow('camera', frame)

    if cv2.waitkey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destrotAllWindow()
