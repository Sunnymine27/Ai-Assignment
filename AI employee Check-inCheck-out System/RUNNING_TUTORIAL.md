# Running Tutorial for the AI Employee Attendance System

This tutorial explains how to run the project step by step.

---

## Step 1: Open a Terminal
Open your terminal or VS Code terminal and go to the project folder:

```bash
cd "/Users/raksachhorn/Documents/AI monday/Ai-Assignment/AI employee Check-inCheck-out System"
```

---

## Step 2: Activate the Correct Python Environment
This project works well with Python 3.12.

```bash
source .venv312/bin/activate
```

If you are creating a new environment, use:

```bash
python3.12 -m venv .venv312
source .venv312/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

---

## Step 3: Start the App
Run the server:

```bash
python app.py
```

You should see output similar to:

```text
AI Employee Check-in/Check-out System
Open http://127.0.0.1:5001 in your browser
```

---

## Step 4: Open the App in Browser
Open:

```text
http://127.0.0.1:5001
```

If port 5000 is occupied, the app will use 5001 automatically.

---

## Step 5: Register an Employee
1. Click Register Employee.
2. Allow webcam access.
3. Capture a face image.
4. Enter the employee details.
5. Click Submit.

---

## Step 6: Check In / Out
1. Open Check In / Out.
2. Allow webcam permission.
3. Click Auto Detect.
4. The system identifies the employee and logs the attendance.

---

## Step 7: View Records
Go to:

- Dashboard
- Records
- Employees

You can see:

- present status
- late arrival status
- attendance list
- CSV exports

---

## Step 8: Stop the App
Press:

```text
Ctrl + C
```

in the terminal to stop the Flask server.

---

## Troubleshooting

### Python version issue
Use Python 3.12 instead of 3.14.

```bash
python --version
```

### Missing dependencies
```bash
python -m pip install -r requirements.txt
```

### Camera not available
- allow webcam access
- ensure no other application is using the camera
- refresh the browser

### Port busy
Try the port printed by the app, usually 5001.

---

## Quick Start Command

```bash
cd "/Users/raksachhorn/Documents/AI monday/Ai-Assignment/AI employee Check-inCheck-out System"
source .venv312/bin/activate
python app.py
```

This is the fastest way to run the project.
