"""
AI Employee Check-in/Check-out System
Flask main application with routes for dashboard, check-in/out, registration, and records.
"""

import os
import pickle
import json
import base64
import socket
import cv2
import numpy as np
from datetime import datetime, date, timedelta
from flask import (
    Flask, render_template, request, jsonify, Response, redirect,
    url_for, flash, send_file
)
import pandas as pd
from database import (
    init_db, add_employee, get_all_employees, get_employee_by_id,
    update_employee, delete_employee, check_in, check_out,
    get_today_attendance, get_attendance_by_date_range,
    get_today_stats, get_weekly_stats, get_employee_check_status,
    get_employee_attendance
)
from face_utils import FaceRecognizer, encode_face_from_base64, save_face_image

app = Flask(__name__)
app.secret_key = 'ai-employee-checkin-checkout-2026'

# Initialize database
init_db()

# Initialize face recognizer
face_recognizer = FaceRecognizer()

# Camera instance (lazy loading)
camera = None


def get_camera():
    """Get or create camera instance."""
    global camera
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return camera


def release_camera():
    """Release camera resource."""
    global camera
    if camera is not None:
        camera.release()
        camera = None


# ─── Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Dashboard — real-time attendance statistics."""
    stats = get_today_stats()
    today_records = get_today_attendance()
    weekly = get_weekly_stats()
    return render_template('index.html',
                           stats=stats,
                           today_records=today_records,
                           weekly=weekly,
                           current_date=date.today().isoformat())


@app.route('/checkin')
def checkin_page():
    """Check-in / Check-out page with webcam."""
    today_records = get_today_attendance()
    return render_template('checkin.html', today_records=today_records)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new employee with face capture."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        department = request.form.get('department', 'General').strip()
        position = request.form.get('position', '').strip()
        face_image_data = request.form.get('face_image', '')

        if not name:
            flash('Employee name is required.', 'error')
            return redirect(url_for('register'))

        if not face_image_data:
            flash('Please capture a face image.', 'error')
            return redirect(url_for('register'))

        # Process face image
        encoding, image = encode_face_from_base64(face_image_data)
        if encoding is None:
            flash('No face detected in the image. Please try again with better lighting.', 'error')
            return redirect(url_for('register'))

        # Save to database
        encoding_bytes = pickle.dumps(encoding)
        employee_id = add_employee(name, department, position, encoding_bytes)

        # Save face image
        if image is not None:
            photo_path = save_face_image(image, employee_id)
            from database import get_db
            conn = get_db()
            conn.execute('UPDATE employees SET photo_path = ? WHERE id = ?',
                         (photo_path, employee_id))
            conn.commit()
            conn.close()

        # Reload face recognizer
        face_recognizer.load_known_faces()

        flash(f'Employee "{name}" registered successfully!', 'success')
        return redirect(url_for('employees'))

    return render_template('register.html')


@app.route('/records')
def records():
    """Attendance records with date filtering."""
    start_date = request.args.get('start_date', (date.today() - timedelta(days=7)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())
    attendance_records = get_attendance_by_date_range(start_date, end_date)
    return render_template('records.html',
                           records=attendance_records,
                           start_date=start_date,
                           end_date=end_date)


@app.route('/employees')
def employees():
    """Employee management page."""
    all_employees = get_all_employees()
    return render_template('employees.html', employees=all_employees)


@app.route('/employee/<int:employee_id>')
def employee_detail(employee_id):
    """Employee detail with attendance history."""
    employee = get_employee_by_id(employee_id)
    if not employee:
        flash('Employee not found.', 'error')
        return redirect(url_for('employees'))
    attendance = get_employee_attendance(employee_id)
    return render_template('employee_detail.html',
                           employee=employee,
                           attendance=attendance)


@app.route('/employee/<int:employee_id>/edit', methods=['POST'])
def edit_employee(employee_id):
    """Update employee details."""
    name = request.form.get('name', '').strip()
    department = request.form.get('department', '').strip()
    position = request.form.get('position', '').strip()

    if name:
        update_employee(employee_id, name, department, position)
        face_recognizer.load_known_faces()
        flash('Employee updated successfully.', 'success')
    else:
        flash('Name is required.', 'error')

    return redirect(url_for('employees'))


@app.route('/employee/<int:employee_id>/delete', methods=['POST'])
def remove_employee(employee_id):
    """Delete (deactivate) an employee."""
    delete_employee(employee_id)
    face_recognizer.load_known_faces()
    flash('Employee removed successfully.', 'success')
    return redirect(url_for('employees'))


# ─── API Routes ──────────────────────────────────────────────────────────

@app.route('/api/recognize', methods=['POST'])
def api_recognize():
    """Recognize face from webcam capture and perform check-in or check-out."""
    data = request.get_json()
    image_data = data.get('image', '')
    action = data.get('action', 'auto')  # 'checkin', 'checkout', or 'auto'

    if not image_data:
        return jsonify({'success': False, 'message': 'No image data provided'})

    # Decode and recognize
    encoding, image = encode_face_from_base64(image_data)
    if encoding is None:
        return jsonify({'success': False, 'message': 'No face detected. Please face the camera directly.'})

    # Compare with known faces
    if not face_recognizer.known_face_encodings:
        return jsonify({'success': False, 'message': 'No employees registered yet.'})

    import face_recognition as fr
    distances = fr.face_distance(face_recognizer.known_face_encodings, encoding)
    best_match_index = np.argmin(distances)

    if distances[best_match_index] >= face_recognizer.tolerance:
        return jsonify({
            'success': False,
            'message': 'Face not recognized. Please register first.'
        })

    employee_id = face_recognizer.known_face_ids[best_match_index]
    employee_name = face_recognizer.known_face_names[best_match_index]
    confidence = round((1.0 - distances[best_match_index]) * 100, 1)

    # Determine action
    status = get_employee_check_status(employee_id)

    if action == 'auto':
        if status == 'not_checked_in':
            action = 'checkin'
        elif status == 'checked_in':
            action = 'checkout'
        else:
            return jsonify({
                'success': False,
                'message': f'{employee_name} has already checked out today.',
                'employee_name': employee_name,
                'confidence': confidence
            })

    if action == 'checkin':
        result = check_in(employee_id)
    else:
        result = check_out(employee_id)

    result['employee_name'] = employee_name
    result['confidence'] = confidence
    result['action'] = action

    return jsonify(result)


@app.route('/api/stats')
def api_stats():
    """Get current attendance statistics as JSON."""
    stats = get_today_stats()
    return jsonify(stats)


@app.route('/api/today')
def api_today():
    """Get today's attendance records as JSON."""
    records = get_today_attendance()
    return jsonify([dict(r) for r in records])


@app.route('/api/weekly')
def api_weekly():
    """Get weekly attendance stats as JSON."""
    weekly = get_weekly_stats()
    return jsonify(weekly)


@app.route('/export')
def export_csv():
    """Export attendance records to CSV."""
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())

    records = get_attendance_by_date_range(start_date, end_date)
    if not records:
        flash('No records to export.', 'error')
        return redirect(url_for('records'))

    data = []
    for r in records:
        data.append({
            'Employee': r['name'],
            'Department': r['department'],
            'Date': r['date'],
            'Check In': r['check_in_time'] or '',
            'Check Out': r['check_out_time'] or '',
            'Status': r['status']
        })

    df = pd.DataFrame(data)
    export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'attendance_export.csv')
    df.to_csv(export_path, index=False)

    return send_file(export_path, as_attachment=True, download_name=f'attendance_{start_date}_to_{end_date}.csv')


# ─── Video Stream (Server-side camera) ──────────────────────────────────

def generate_frames():
    """Generate video frames with face recognition overlay."""
    cam = get_camera()
    frame_count = 0

    while True:
        success, frame = cam.read()
        if not success:
            break

        # Only run recognition every 3 frames for performance
        if frame_count % 3 == 0:
            results = face_recognizer.recognize_faces(frame)
            frame = face_recognizer.annotate_frame(frame, results)

        frame_count += 1

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route for server-side camera."""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


# ─── Template Filters ───────────────────────────────────────────────────

@app.template_filter('format_time')
def format_time(value):
    """Format ISO timestamp to readable time."""
    if not value:
        return '—'
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%I:%M %p')
    except (ValueError, TypeError):
        return value


@app.template_filter('format_datetime')
def format_datetime(value):
    """Format ISO timestamp to readable date and time."""
    if not value:
        return '—'
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%b %d, %Y %I:%M %p')
    except (ValueError, TypeError):
        return value


@app.template_filter('format_date')
def format_date(value):
    """Format date string to readable format."""
    if not value:
        return '—'
    try:
        d = date.fromisoformat(value)
        return d.strftime('%b %d, %Y')
    except (ValueError, TypeError):
        return value


# ─── Main ────────────────────────────────────────────────────────────────

def find_available_port(start_port=5000, max_attempts=20):
    """Return the first free local port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if sock.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return start_port


if __name__ == '__main__':
    # Create required directories
    os.makedirs('known_faces', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

    port = find_available_port(5000, 20)
    print("\n" + "=" * 60)
    print("  AI Employee Check-in/Check-out System")
    print(f"  Open http://127.0.0.1:{port} in your browser")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=port)
