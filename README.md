
# Face Detection Attendance System

This project is a **Face Detection Attendance System** built using Python, OpenCV (`cv2`), `cvzone` for easier face detection, and Firebase as the database. The system detects faces in real-time and records attendance by storing the data in Firebase.

## Features

- **Real-time Face Detection** using OpenCV and cvzone.
- **Attendance Recording**: Automatically records attendance when a face is detected.
- **Firebase Integration**: Stores attendance data in Firebase, a real-time NoSQL cloud database.
- **User-friendly Interface** for administrators to track attendance.

## Technologies Used

- **Python**: Core programming language.
- **OpenCV (cv2)**: For face detection and image processing.
- **cvzone**: Simplifies the face detection process using OpenCV.
- **Firebase**: Cloud storage for attendance data.
  
## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Firebase account (for database storage)
- Google Cloud Service Account key (for Firebase authentication)

### Clone the Repository

```bash
git clone https://github.com/Waseem-Baig/Face_Detection_Attendance.git
cd Face_Detection_Attendance
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure to include the following libraries in your `requirements.txt`:

```
opencv-python
cvzone
firebase-admin
```

### Firebase Setup

1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Create a new project.
3. Set up **Firestore** or **Realtime Database**.
4. Download the `serviceAccountKey.json` from your Firebase project settings and place it in your project directory.
5. Update the Firebase initialization code in your project to reference this key.

### Running the Project

```bash
python main.py
```

The program will start detecting faces through your webcam and will log attendance data in Firebase.

## Folder Structure

```
|-- Face_Detection_Attendance/
    |-- main.py               # Main application script
    |-- serviceAccountKey.json # Firebase authentication key
    |-- attendance.csv         # Local attendance log (if applicable)
    |-- README.md              # This file
    |-- .gitignore             # Ignored files (e.g., serviceAccountKey.json)
```

## Usage

1. Run the program to start face detection.
2. The system will detect faces and automatically log attendance data.
3. You can monitor attendance records in your Firebase project.

## Contributing

Feel free to fork the repository, create a new branch, and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
