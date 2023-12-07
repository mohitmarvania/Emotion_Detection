"""
This is the testing module.
After completing the training on the given faces data run this module
to get the result on the live camera feed.
"""

import cv2
import numpy as np
from keras.models import model_from_json


# FUNCTION WHICH CALCULATE THE TOTAL PERCENTAGE.
def percentage(x, total):
    percent = x / total
    percent = int(percent * 100)
    return percent


def store_percent(a, d, f, h, n, sa, su):
    # dict = {"Angry": a, "Disgusted": d, "Fearful": f, "Happy": h, "Neutral": n, "Sad": sa, "Surprised": su}
    dicty = {a: "Angry", d: "Disgusted", f: "Fearful", h: "Happy", n: "Neutral", sa: "Sad", su: "Surprised"}

    maximum = max(a, d, f, h, n, sa, su)
    return dicty[maximum]


def test_emotion():
    # Dictionary for all emotions.
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    # Load json and create model
    json_file = open('Model/emotional_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    emotion_model = model_from_json(loaded_model_json)

    # Load weights into new model
    emotion_model.load_weights("Model/emotional_model.h5")
    print("LOADED MODEL FROM DISK!!")

    # Start the webcam feed
    camera = cv2.VideoCapture(0)
    total_faces = []
    total_frames = 0

    # Lists to store each emotion count.
    Angry = 0
    Disgusted = 0
    Fearful = 0
    Happy = 0
    Neutral = 0
    Sad = 0
    Surprised = 0

    while True:
        # Finding haar cascade to draw bounding box around face
        ret, frame = camera.read()
        frame = cv2.resize(frame, (1280, 720))
        if not ret:
            break
        # -------------OVERHERE PROVIDE THE PATH OF THE "HAARCASCADE_FRONTALFACE_DEFAULT.XML" FILE FROM THE
        # HAARCASCADE FOLDER.------------
        face_detector = cv2.CascadeClassifier(
            '/Users/mohit/PycharmProjects/Emotion_detection/haarcascade/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces available on camera
        num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and Preprocess it
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y: y + h, x: x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            if len(num_faces) not in total_faces:
                total_faces.append(len(num_faces))

            # PREDECTING THE EMOTIONS
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            total_frames += 1

            # Increase count of captured emotion
            if emotion_dict[maxindex] == "Angry":
                Angry += 1
            elif emotion_dict[maxindex] == "Disgusted":
                Disgusted += 1
            elif emotion_dict[maxindex] == "Fearful":
                Fearful += 1
            elif emotion_dict[maxindex] == "Happy":
                Happy += 1
            elif emotion_dict[maxindex] == "Sad":
                Sad += 1
            elif emotion_dict[maxindex] == "Surprised":
                Surprised += 1
            elif emotion_dict[maxindex] == "Neutral":
                Neutral += 1
            else:
                continue

            cv2.putText(frame, emotion_dict[maxindex], (x + 5, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                        cv2.LINE_AA)

        cv2.imshow('Emotion Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Faces detected : {}".format(max(total_faces)))

    # Calculate percentage and store it in the variable
    angry = percentage(Angry, total_frames)
    disgusted = percentage(Disgusted, total_frames)
    fearful = percentage(Fearful, total_frames)
    happy = percentage(Happy, total_frames)
    sad = percentage(Sad, total_frames)
    surprised = percentage(Surprised, total_frames)
    neutral = percentage(Neutral, total_frames)

    # Print the percentage of the emotions
    print("-------------------------------------------")
    print("Angry : {} %".format(angry))
    print("Disgusted : {} %".format(disgusted))
    print("Fearful : {} %".format(fearful))
    print("Happy : {} %".format(happy))
    print("Sad : {} %".format(sad))
    print("Surprised : {} %".format(surprised))
    print("Neutral : {} %".format(neutral))
    print("-------------------------------------------")

    # Show the highest percent emotion.
    # print(max(angry, disgusted, fearful, happy, sad, surprised, neutral))
    final_emotion = store_percent(angry, disgusted, fearful, happy, neutral, sad, surprised)
    print(final_emotion)
    print("Total frames recorded : {}".format(total_frames))

    camera.release()
    cv2.destroyAllWindows()
    return final_emotion
