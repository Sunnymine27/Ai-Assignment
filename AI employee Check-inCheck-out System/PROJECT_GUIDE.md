# AI Employee Check-in/Check-out System - Project Guide

## 1. Project Overview

This project is a Flask-based employee attendance system that uses AI face recognition to identify employees and record their check-in and check-out times automatically.

It is designed for small office or classroom attendance management, where the supervisor can:

- register employees
- capture their face image
- track attendance records
- view dashboard statistics
- export attendance as CSV
- check whether an employee is present, late, or absent

The system is built using:

- Python
- Flask
- OpenCV
- face_recognition
- SQLite
- HTML/CSS/JavaScript

---

## 2. Main Functionalities

### Dashboard
The dashboard shows:

- total number of employees
- present employees today
- absent employees today
- late arrivals
- weekly attendance trends
- recent activity

### Employee Registration
A user can register each employee by:

- entering the employee name
- selecting department
- entering designation or position
- capturing a face image from the webcam
- storing the face encoding in the database

### Face Recognition Check-in / Check-out
The system compares the camera feed with stored face encodings. If a user is recognized:

- if they are not checked in, the system marks them as checked in
- if they are already checked in, it marks them as checked out
- it prevents duplicate check-ins for the same day
- it flags late attendance based on the time

### Attendance Records
The records page allows the user to:

- view daily or date-range attendance
- search attendance history
- export records to CSV

---

## 3. Project Structure

```text
AI employee Check-inCheck-out System/
├── app.py                     # Main Flask application
├── database.py                # SQLite database logic
├── face_utils.py              # Face detection and recognition tools
├── requirements.txt           # Dependency list
├── attendance.db              # SQLite database file
├── attendance_export.csv      # CSV export file (generated when exported)
├── known_faces/               # Stored employee face images
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── checkin.html
│   ├── register.html
│   ├── records.html
│   ├── employees.html
│   └── employee_detail.html
├── README.md
├── PROJECT_GUIDE.md
├── RUNNING_TUTORIAL.md
└── README.txt.txt
```

---

## 4. Tech Stack Explained

### Flask
Flask is the web framework used to create the system interface and routes.

It handles:

- page rendering
- API requests
- webcam capture requests
- database interactions
- attendance logic

### OpenCV
OpenCV is used to process webcam frames, detect faces, and save images.

### face_recognition
This library compares captured face images with stored employee encodings.
It finds and matches facial features using machine learning-based embeddings.

### SQLite
SQLite is the database engine used to store:

- employee information
- face encodings
- attendance records
- timestamps

### HTML, CSS, and JavaScript
These are used for the user interface and front-end interactivity such as:

- webcam display
- JavaScript-based face capture
- chart rendering
- dynamic data refresh

---

## 5. How the System Works

### Step 1: Register Employee
When an employee is added:

1. the user captures a face image from the browser
2. the image is decoded from base64
3. OpenCV and face_recognition detect the face
4. a face encoding is generated
5. the encoding is saved to SQLite
6. the image is saved to the known_faces folder

### Step 2: Check-In / Check-Out
When the user chooses Auto Detect:

1. the webcam captures an image
2. the system detects a face in the image
3. it compares the face to all registered encodings
4. the closest match is selected
5. the employee is identified
6. the system checks whether they are already checked in today
7. it records the correct action (check-in or check-out)

### Step 3: Attendance Logic
The system uses the current date and time to decide:

- if the employee is checked in or out
- if a check-in is done after 8:00 AM, it is marked as late
- if an employee has already checked in for the day, the system blocks duplicate check-ins

---

## 6. Installation Requirements

### Required Software

- Python 3.12 (recommended)
- pip
- webcam/camera
- CMake (sometimes needed by the face-recognition toolchain)

### Why Python 3.12?
This project uses the classic face_recognition library, which is known to be more compatible with Python 3.12 than with Python 3.14.

Using Python 3.12 avoids common import and package compatibility issues.

---

## 7. Step-by-Step Setup

### Option A: Use the project virtual environment already created
If the environment is already present in the project folder, run:

```bash
cd "/Users/raksachhorn/Documents/AI monday/Ai-Assignment/AI employee Check-inCheck-out System"
source .venv312/bin/activate
python app.py
```

### Option B: Create a new virtual environment
```bash
cd "/Users/raksachhorn/Documents/AI monday/Ai-Assignment/AI employee Check-inCheck-out System"
python3.12 -m venv .venv312
source .venv312/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python app.py
```

---

## 8. How to Run the Application

After installing dependencies, start the app:

```bash
cd "/Users/raksachhorn/Documents/AI monday/Ai-Assignment/AI employee Check-inCheck-out System"
source .venv312/bin/activate
python app.py
```

Then open this in your browser:

```text
http://127.0.0.1:5001
```

Note: port 5000 may be occupied on macOS due to AirPlay/AirTunes, so the app may use 5001 instead.

---

## 9. How to Use the App

### Register an Employee
1. Open the app.
2. Click Register Employee.
3. Allow webcam access.
4. Capture a clear face image.
5. Fill in:
   - name
   - department
   - position
6. Click submit.

### Check In / Out
1. Go to Check In / Out.
2. Allow webcam access.
3. Click Auto Detect.
4. The system detects the person and performs the correct action.

### Dashboard
The dashboard provides a quick evaluation of:

- who is present
- who is absent
- who is late
- weekly attendance

### Records
The attendance page lets you:

- review records by date range
- filter data
- export CSV files

---

## 10. Common Issues and Fixes

### Issue: App does not start
Check the Python version:

```bash
python --version
```

If it is Python 3.14, switch to Python 3.12.

### Issue: face_recognition errors
Install the required model package and use a supported Python version:

```bash
python -m pip install "setuptools<81"
python -m pip install git+https://github.com/ageitgey/face_recognition_models
```

### Issue: Port already in use
If 5000 is busy, the app may start on 5001 automatically. Use that URL instead.

### Issue: Camera is not working
- allow webcam permissions
- ensure no other app is using the camera
- refresh the browser page

---

## 11. Troubleshooting Summary

If the app fails to run:

1. confirm Python version is 3.12
2. activate the correct virtual environment
3. install requirements
4. confirm the browser has camera access
5. use the port printed in the terminal

---

## 12. Final Notes

This project is a practical student project that demonstrates:

- AI-based face recognition
- Flask web development
- attendance tracking automation
- database management
- dashboard reporting

It is suitable for learning and demonstration, especially in academic or assignment projects.

---

## 13. Useful Commands

```bash
cd "/Users/raksachhorn/Documents/AI monday/Ai-Assignment/AI employee Check-inCheck-out System"
source .venv312/bin/activate
python app.py
```

```bash
python -m pip install -r requirements.txt
```

```bash
python -m pip install "setuptools<81"
```

---

If you want to submit this project, you can also use this guide as part of your documentation package, assignment write-up, or README explanation.
