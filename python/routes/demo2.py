import cv2
import numpy as np
from datetime import datetime
from queue import Empty

def genderDetection(frameQueue, stopFlag):
    face_net = cv2.dnn.readNetFromCaffe('./routes/deploy.prototxt', './routes/res10_300x300_ssd_iter_140000.caffemodel')
    gender_net = cv2.dnn.readNetFromCaffe('./routes/deploy_gender.prototxt', './routes/gender_net.caffemodel')

    gender_list = ['Male', 'Female']

    while not stopFlag.is_set():
        try:
            frame = frameQueue.get()
        except Empty:
            continue

        if frame is None or stopFlag.is_set():
            break

        if frame is not None:
            male_count = 0
            female_count = 0

            current_hour = datetime.now().hour
            is_night = current_hour >= 19 or current_hour < 6

            h, w = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            face_net.setInput(blob)
            detections = face_net.forward()

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    face = frame[startY:endY, startX:endX]

                    face_blob = cv2.dnn.blobFromImage(cv2.resize(face, (227, 227)), 1.0, (227, 227),
                                                    (78.4263377603, 87.7689143744, 114.895847746))


                    gender_net.setInput(face_blob)
                    gender_preds = gender_net.forward()
                    gender_index = gender_preds[0].argmax()
                    gender = gender_list[gender_index]

                    if gender_index == 0:
                        male_count += 1
                    else:
                        female_count += 1

                    label = f"{gender}: {confidence:.2f}"
                    color = (0, 255, 0) if gender_index == 0 else (255, 0, 0)

                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                    cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            count_label = f"Males: {male_count}, Females: {female_count}"
            cv2.putText(frame, count_label, (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            if is_night and female_count == 1 and male_count == 0:
                warning_text = "ALERT: Lone woman detected at night!"
                cv2.putText(frame, warning_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.imshow("Gender Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
