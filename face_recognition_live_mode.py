import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime


def aut():
    path = 'images'
    if len(os.listdir(path)) != 0:
        csv_filename = 'registered_people.csv'

        def read_line_by_index(csv_filename, index):
            with open(csv_filename, 'r', encoding='utf-8') as file:
                for i, line in enumerate(file):
                    if i == index:
                        return line.strip()

        images = []
        classNames = []
        myList = os.listdir(path)

        for cl in myList:
            images.append(cv2.imread(f"{path}/{cl}"))
            classNames.append(os.path.splitext(cl)[0])


        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList


        def markAttendance(name):
            with open('attendance.csv', 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f"\n{name},{dtString}")


        encodeListKnown = findEncodings(images)


        cap = cv2.VideoCapture(0)

        res = True
        res1 = None
        while res:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                print(faceDis)
                mathIndex = np.argmin(faceDis)
                name = classNames[mathIndex].upper()

                if matches[mathIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)
                else:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)

                cv2.imshow('Webcam', img)
                cv2.waitKey(1)
                counter = 0
                for i in faceDis:
                    if i <= 0.35:
                        result = read_line_by_index(csv_filename, counter)
                        res = False
                        res1 = (True, name, i, result)
                        break
                    counter += 1

        return res1
    else:
        return [False]