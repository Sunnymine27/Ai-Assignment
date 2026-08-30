# 🤖 AI Employee Check-in/Check-out System

A Python Flask-based employee attendance system using **AI face recognition** via webcam. The system detects and identifies employees in real-time, automatically recording check-in and check-out times.

## ✨ Features

### 1. AI Status Analysis & Real-time Dashboard
- Live attendance statistics (present, absent, late arrivals)
- Weekly attendance chart with Chart.js
- Today's breakdown donut chart
- Real-time activity feed
- Auto-refreshing stats every 30 seconds

### 2. AI Attendance System via Camera
- Server-side camera with real-time face recognition overlay
- Bounding boxes with employee names and confidence scores
- Live video streaming through Flask

### 3. AI Employee Check-in/Check-out Recording
- Browser-based webcam face capture
- Automatic face recognition and identity matching
- Smart auto-detect: checks in if not checked in, checks out if already in
- Duplicate prevention (one check-in/check-out per day)
- Late detection (after 8:00 AM)
- Attendance records with date filtering
- CSV export

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.9+, Flask |
| Face Detection | OpenCV |
| Face Recognition | face_recognition (dlib) |
| Database | SQLite |
| Frontend | HTML/CSS/JS, Chart.js |
| Data Export | pandas |

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- CMake (required for dlib/face_recognition)
- Webcam

### macOS Setup
```bash
# Install CMake
brew install cmake

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Windows Setup
```bash
# Install CMake from https://cmake.org/download/

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Running the Application

```bash
# Activate virtual environment (if not already)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run the application
python app.py
```

Open your browser and go to: **http://127.0.0.1:5000**

## 📖 Usage

### 1. Register Employees
- Navigate to **Register Employee**
- Start the camera and capture a face photo
- Fill in name, department, and position
- Submit to register

### 2. Check In / Check Out
- Navigate to **Check In / Out**
- Start the camera
- Click **Auto Detect** — the system will:
  - ✅ **Check In** if the employee hasn't checked in yet
  - 🔄 **Check Out** if the employee is already checked in
- Or use the manual **Check In** / **Check Out** buttons

### 3. View Dashboard
- Navigate to **Dashboard** for real-time stats
- View weekly charts, today's breakdown, and recent activity

### 4. Attendance Records
- Navigate to **Attendance Records**
- Filter by date range
- Export to CSV

## 📁 Project Structure

```
AI employee Check-inCheck-out System/
├── app.py                 # Flask main application
├── database.py            # SQLite database operations
├── face_utils.py          # Face recognition utilities
├── requirements.txt       # Python dependencies
├── known_faces/           # Stored employee face images
├── static/
│   ├── css/style.css      # Styling
│   └── js/main.js         # Frontend JavaScript
├── templates/
│   ├── base.html          # Base layout
│   ├── index.html         # Dashboard
│   ├── checkin.html       # Check-in/out page
│   ├── register.html      # Employee registration
│   ├── records.html       # Attendance records
│   ├── employees.html     # Employee management
│   └── employee_detail.html
└── README.md
```

## 👥 Authors

- Student Group Assignment
- Date: 7/19/2026
- Instructor: LEANG PANHRA

## 📄 License

This project is for educational purposes.
