import cv2
import os
import numpy as np
from keras.models import load_model
from src.mqtt_client import MQTTClient
from src.sound_alarm import SoundAlarm
from src.utils import preprocess_eye, draw_rectangles

def run_detector():
    # Initialize paths
    base_path = os.getcwd()
    alarm_path = os.path.join(base_path, 'alarms', 'alarm.wav')
    model_path = os.path.join(base_path, 'models', 'CNN__model.h5')
    cascades_path = os.path.join(base_path, 'cascades')

    # Load cascade classifiers
    face_cascade = cv2.CascadeClassifier(os.path.join(cascades_path, 'haarcascade_frontalface_alt.xml'))
    leye_cascade = cv2.CascadeClassifier(os.path.join(cascades_path, 'haarcascade_lefteye_2splits.xml'))
    reye_cascade = cv2.CascadeClassifier(os.path.join(cascades_path, 'haarcascade_righteye_2splits.xml'))
    eyes_cascade = cv2.CascadeClassifier(os.path.join(cascades_path, 'haarcascade_eye.xml'))

    # Load CNN model
    model = load_model(model_path)

    # Initialize sound alarm and MQTT client
    alarm = SoundAlarm(alarm_path)
    mqtt_client = MQTTClient()

    # Open webcam
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    score = 0
    thicc = 2

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25,25))
        eyes = eyes_cascade.detectMultiScale(gray)
        left_eye = leye_cascade.detectMultiScale(gray)
        right_eye = reye_cascade.detectMultiScale(gray)

        # Draw rectangles for detected faces and eyes
        draw_rectangles(frame, faces)
        draw_rectangles(frame, eyes)

        rpred = [99]
        lpred = [99]

        # Process right eye
        for (x, y, w, h) in right_eye:
            r_eye_img = frame[y:y+h, x:x+w]
            r_eye_input = preprocess_eye(r_eye_img)
            rpred = (model.predict(r_eye_input) > 0.5).astype("int32")
            break

        # Process left eye
        for (x, y, w, h) in left_eye:
            l_eye_img = frame[y:y+h, x:x+w]
            l_eye_input = preprocess_eye(l_eye_img)
            lpred = (model.predict(l_eye_input) > 0.5).astype("int32")
            break

        # Determine eye status and update score
        if rpred[0] == 0 and lpred[0] == 0:
            score += 1
            cv2.putText(frame, "Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            score -= 1
            cv2.putText(frame, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        if score < 0:
            score = 0

        cv2.putText(frame, f'Score: {score}', (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        if score > 10:
            mqtt_client.publish_sleep_alert()

            # Save alert image
            cv2.imwrite(os.path.join(base_path, 'results', 'sleep_alert_image.jpg'), frame)

            # Play alarm sound
            alarm.play()

            if thicc < 16:
                thicc += 2
            else:
                thicc -= 2
                if thicc < 2:
                    thicc = 2

            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)
        else:
            alarm.stop()

        cv2.imshow('Driver Drowsiness Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_detector()
