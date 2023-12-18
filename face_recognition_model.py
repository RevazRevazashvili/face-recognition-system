import cv2
import face_recognition

# load images
new_size = (800, 800)


def face_location(face):
    return face_recognition.face_locations(face)[0]


def face_encode(face):
    return face_recognition.face_encodings(face)[0]


def make_rectangle(img, color=(255, 0, 255)):
    return cv2.rectangle(img, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), color, 2)


myImg = cv2.resize(cv2.cvtColor(face_recognition.load_image_file("images/revaz.jpg"), cv2.COLOR_BGR2RGB), new_size)

myImgTest = cv2.resize(cv2.cvtColor(face_recognition.load_image_file("images/revaz1.jpg"), cv2.COLOR_BGR2RGB), new_size)

faceLoc = face_location(myImg)
encodeMyImg = face_encode(myImg)
make_rectangle(myImg)

faceLocTest = face_location(myImgTest)
encodeMyImgTest = face_encode(myImgTest)
make_rectangle(myImgTest)

result = face_recognition.compare_faces([encodeMyImg], encodeMyImgTest)
faceDist = face_recognition.face_distance([encodeMyImg], encodeMyImgTest)


if result[0]:
    make_rectangle(myImgTest, (0, 153, 0))
else:
    make_rectangle(myImgTest, (0, 0, 255))
cv2.putText(myImgTest, f'{result} {round(faceDist[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
cv2.imshow("revaz", myImg)
cv2.imshow("revaz2", myImgTest)

cv2.waitKey(0)
