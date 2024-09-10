import pickle
import cv2
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-f3445-default-rtdb.firebaseio.com/",
    'storageBucket': "face-attendance-f3445.appspot.com"
})

# Supported image extensions
valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}

# Importing the students' images
folderPath = "Images"
pathList = [file for file in os.listdir(folderPath) if os.path.splitext(file)[1].lower() in valid_extensions]

# Load images and extract student IDs
imgList = []
studentIDS = []
for path in pathList:
    full_path = os.path.join(folderPath, path)
    imgList.append(cv2.imread(full_path))
    studentIDS.append(os.path.splitext(path)[0])

    fileName = f"{folderPath}/{path}"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


def findEncodings(imagesList):
    encodeList = []
    for image in imagesList:
        # Ensure image is in RGB format
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Find face encodings
        encodings = face_recognition.face_encodings(rgb_image)
        if encodings:
            encodeList.append(encodings[0])
        else:
            print("No faces found in one of the images.")
    return encodeList


encodeListKnown = findEncodings(imgList)
encodeListKnownWithIDS = [encodeListKnown, studentIDS]
print(encodeListKnown)

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithIDS, file)
file.close()
