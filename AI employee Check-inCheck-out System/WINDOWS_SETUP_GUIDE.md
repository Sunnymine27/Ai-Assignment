# Windows Setup Guide for AI Employee Check-in/Check-out System

This project is a Flask-based employee attendance system with AI face recognition. It uses OpenCV, face_recognition, and SQLite.

This guide is written for Windows users and focuses on the setup steps that usually cause problems.

## Requirements

Before starting, make sure you have:

- Windows 10 or Windows 11
- Python 3.12 installed
- Git installed (optional, but useful)
- Webcam connected
- Administrator access for installing build tools

## Important note about Python version

Use Python 3.12 for this project.

The face_recognition library is sensitive to Python versions and can fail on Python 3.14 or newer. Python 3.12 is the safest option for this app.

## Step 1: Install Python 3.12

1. Go to the official Python website:
   https://www.python.org/downloads/
2. Download Python 3.12.
3. During installation, check these options:
   - Add Python to PATH
   - Install launcher for all users
4. Finish the installation.

To verify:

```powershell
python --version
```

You should see something like:

```text
Python 3.12.x
```

## Step 2: Install CMake

1. Download CMake from:
   https://cmake.org/download/
2. Install it.
3. Make sure the CMake bin folder is added to your PATH.

Check it with:

```powershell
cmake --version
```

## Step 3: Install Visual Studio Build Tools

This is required for compiling dlib and face_recognition on Windows.

1. Install Visual Studio Community.
2. During installation, add the workload:
   - Desktop development with C++
3. Also make sure these components are selected:
   - MSVC C++ x64/x86 build tools
   - Windows 10/11 SDK

If the installation fails later, this is usually the missing part.

## Step 4: Open PowerShell in the project folder

Open PowerShell and navigate to the project directory.

Example:

```powershell
cd "C:\path\to\AI employee Check-inCheck-out System"
```

## Step 5: Create a virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Step 6: Upgrade pip and install dependencies

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install cmake
pip install -r requirements.txt
```

If face_recognition or dlib fails to install, try this:

```powershell
pip install --upgrade setuptools
pip install "setuptools<70"
pip install -r requirements.txt
```

## Step 7: Run the project

From the project folder, with the virtual environment active:

```powershell
python app.py
```

The app should start and show a local address like:

```text
http://127.0.0.1:5000
```

If port 5000 is busy, the app may choose another free port such as 5001.

Open the printed URL in your browser.

## Step 8: Use the app

After the app loads:

1. Go to the employee registration page.
2. Register a new employee.
3. Use the webcam to capture a face image.
4. Save the employee.
5. Open the check-in/check-out page.
6. Use the webcam to detect and verify attendance.
7. View dashboard statistics and attendance records.

## Common issues and fixes

### Issue: PowerShell blocks script activation

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### Issue: face_recognition fails to install

Install Visual Studio C++ Build Tools and retry:

```powershell
pip install -r requirements.txt
```

### Issue: dlib fails to build

Make sure both of these are installed:

- Python 3.12
- Visual Studio Desktop C++ workload

### Issue: Python version mismatch

Check:

```powershell
python --version
```

If it is not 3.12, install 3.12 and recreate the virtual environment.

### Issue: port already in use

The app may automatically select another free port. If it does not, change the port in the app startup code and run it again.

## Quick copy-paste setup command list

```powershell
cd "C:\path\to\AI employee Check-inCheck-out System"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install cmake
pip install -r requirements.txt
python app.py
```

## Final checklist

Before running the app, ensure:

- Python 3.12 is installed
- Virtual environment is created
- Required dependencies are installed
- CMake is installed
- Visual Studio C++ build tools are installed
- Webcam is working

## Summary

This project is a Flask + OpenCV + face-recognition application. On Windows, the main setup requirements are:

- Python 3.12
- CMake
- Visual Studio C++ Build Tools
- a virtual environment
- webcam access

Once those are installed correctly, the app should run smoothly.
