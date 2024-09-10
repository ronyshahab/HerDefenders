import cv2
import threading
from routes.demo2 import genderDetection
from routes.gesture import threatDetection
from queue import Queue


def multiThreadingCalls(stopFlag):
    frameQueue = Queue()
    
    def capture_video(frameQueue):
        cap = cv2.VideoCapture(0) 
        while not stopFlag.is_set():
            ret, frame = cap.read()
            if not ret:
                break
            frameQueue.put(frame)  
        frameQueue.put(None)

        cap.release()

    capture_thread = threading.Thread(target=capture_video, args=(frameQueue,))
    processing_thread_1 = threading.Thread(target=genderDetection, args=(frameQueue,stopFlag))
    processing_thread_2 = threading.Thread(target=threatDetection, args=(frameQueue,stopFlag))
    
    capture_thread.start()
    processing_thread_1.start()
    processing_thread_2.start()
    
    cv2.destroyAllWindows()
    
    capture_thread.join()
    processing_thread_1.join()
    processing_thread_2.join()
