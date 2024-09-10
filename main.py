import os
import pickle
import cv2
import cvzone
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-f3445-default-rtdb.firebaseio.com/",
    'storageBucket': "face-attendance-f3445.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

imageBackground = cv2.imread("Resources/background.png")

# Importing the mode images into a list
folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Import the encoding file
with open("EncodeFile.p", "rb") as file:
    encodeListKnownWithIDS = pickle.load(file)
    encodeListKnown, studentIDS = encodeListKnownWithIDS

modeType = 0
counter = 0
sid = -1
attendance = 0
name = ""
branch = ""
standing = ""
starting_year = 0
year = ""
imgStudent = []

print(studentIDS)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame from the webcam.")
        break

    # Resize image for faster processing (Try different resize ratios if needed)
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Adjust resize ratio as needed
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Debugging: print the size of the resized image
    # print(f"Resized image shape: {imgS.shape}")

    try:
        # Find faces and encodings
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        # Debugging: print the number of faces found
        # print(f"Number of faces detected: {len(faceCurFrame)}")

    except Exception as e:
        print(f"Error during face detection: {e}")
        continue

    # Verify dimensions of the image being assigned
    if img.shape[0] == 480 and img.shape[1] == 640:
        imageBackground[162:162 + 480, 55:55 + 640] = img
    else:
        print(f"Warning: Camera frame size is {img.shape}, expected 640x480")

    # Resize the mode image to the expected size (633x434)
    resizedModeImage = cv2.resize(imgModeList[modeType], (434, 633))
    imageBackground[44:44 + 633, 808:808 + 434] = resizedModeImage

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            # Debugging: print the matches and distances
            print(f"Matches: {matches}")
            print(f"Distances: {faceDis}")

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imageBackground, bbox=bbox, rt=0)

                sid = studentIDS[matchIndex]
                if counter == 0:
                    counter = 1
                    modeType = 1
                # print("Known Face detected")
                # print(studentIDS[matchIndex])

            if counter != 0:
                if counter == 1:
                    studentInfo = db.reference(f"Students/{sid}").get()
                    print(studentInfo)
                    attendance = studentInfo['total_attendance']
                    name = studentInfo['name']
                    branch = studentInfo['branch']
                    standing = studentInfo['standing']
                    starting_year = studentInfo['starting_year']
                    year = studentInfo['year']
                    last_attendance_time = studentInfo['last_attendance_time']

                    blob = bucket.get_blob(f"Images/{sid}.png")
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                    datetimeObject = datetime.datetime.strptime(last_attendance_time, "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.datetime.now() - datetimeObject).total_seconds()

                    if secondsElapsed > 30:
                        ref = db.reference(f"Students/{sid}")
                        attendance += 1
                        ref.child('total_attendance').set(attendance)
                        ref.child('last_attendance_time').set(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        counter = 0
                        resizedModeImage = cv2.resize(imgModeList[modeType], (434, 633))
                        imageBackground[44:44 + 633, 808:808 + 434] = resizedModeImage
                if modeType != 3:
                    if 8 < counter <= 15:
                        modeType = 2

                    resizedModeImage = cv2.resize(imgModeList[modeType], (434, 633))
                    imageBackground[44:44 + 633, 808:808 + 434] = resizedModeImage

                    if counter <= 8:
                        cv2.putText(imageBackground, str(attendance), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imageBackground, str(branch), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imageBackground, str(sid), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imageBackground, str(standing), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imageBackground, str(year), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imageBackground, str(starting_year), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        (w, h), _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (440 - w) // 2
                        cv2.putText(imageBackground, str(name), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        imageBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter > 15:
                    counter = 0
                    modeType = 0
                    studentInfo = {}
                    imgStudent = []
                    resizedModeImage = cv2.resize(imgModeList[modeType], (434, 633))
                    imageBackground[44:44 + 633, 808:808 + 434] = resizedModeImage
    else:
        modeType = 0
        counter = 0
    cv2.imshow("Face Attendance", imageBackground)

    # Adjust waitKey for desired frame rate and allow exit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
