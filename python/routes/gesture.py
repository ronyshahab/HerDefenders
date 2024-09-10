import cv2
import mediapipe as mp
import numpy as np
from queue import Empty

def threatDetection(frameQueue, stopFlag):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    HELP_GESTURE = [1, 1, 1, 1, 1]  

    def get_finger_states(hand_landmarks):
        finger_states = []
        tips = [4, 8, 12, 16, 20]
        for i, tip in enumerate(tips):
            if i == 0:
                if hand_landmarks.landmark[tip].x < hand_landmarks.landmark[tip - 1].x:
                    finger_states.append(1)
                else:
                    finger_states.append(0)
            else:
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                    finger_states.append(1)
                else:
                    finger_states.append(0)
        return finger_states

    def detect_gesture(finger_states):
        if finger_states == HELP_GESTURE:
            return "HELP"
        return None
    while not stopFlag.is_set():
        try: 
            frame = frameQueue.get()
        except Empty:
            continue

        if frame is None or stopFlag.is_set():
            break

        if frame is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    finger_states = get_finger_states(hand_landmarks)
                    gesture = detect_gesture(finger_states)

                    if gesture:
                        cv2.putText(frame, f"Gesture Detected: {gesture}", (10, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


            cv2.imshow('Hand Gesture Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    hands.close()
