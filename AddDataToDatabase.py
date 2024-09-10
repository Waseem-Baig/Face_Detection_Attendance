import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-f3445-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "321654":
        {
            "name": "Shaik Azeem",
            "branch": "CSE",
            "starting_year": 2022,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-09-05 22:50:00"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "branch": "ECE",
            "starting_year": 2021,
            "total_attendance": 10,
            "standing": "A",
            "year": 3,
            "last_attendance_time": "2024-09-05 22:50:00"
        },
    "963852":
        {
            "name": "Elon Musk",
            "branch": "EEE",
            "starting_year": 2020,
            "total_attendance": 12,
            "standing": "B",
            "year": 4,
            "last_attendance_time": "2024-09-05 22:50:00"
        },
    "123456":
        {
            "name": "Waseem Baig",
            "branch": "CSE",
            "starting_year": 2022,
            "total_attendance": 15,
            "standing": "S",
            "year": 3,
            "last_attendance_time": "2024-09-05 22:50:00"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
