"""
Database module for AI Employee Check-in/Check-out System.
Handles SQLite database setup, employee and attendance CRUD operations.
"""

import sqlite3
import os
from datetime import datetime, date

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'attendance.db')


def get_db():
    """Get a database connection with row factory."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_db()
    cursor = conn.cursor()

    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT DEFAULT 'General',
            position TEXT DEFAULT '',
            face_encoding BLOB,
            photo_path TEXT DEFAULT '',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')

    # Create attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            check_in_time TIMESTAMP,
            check_out_time TIMESTAMP,
            date TEXT NOT NULL,
            status TEXT DEFAULT 'present',
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')

    conn.commit()
    conn.close()


# ─── Employee Operations ────────────────────────────────────────────────

def add_employee(name, department, position, face_encoding_bytes, photo_path=''):
    """Add a new employee to the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO employees (name, department, position, face_encoding, photo_path)
           VALUES (?, ?, ?, ?, ?)''',
        (name, department, position, face_encoding_bytes, photo_path)
    )
    employee_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return employee_id


def get_all_employees(active_only=True):
    """Get all employees."""
    conn = get_db()
    cursor = conn.cursor()
    if active_only:
        cursor.execute('SELECT * FROM employees WHERE is_active = 1 ORDER BY name')
    else:
        cursor.execute('SELECT * FROM employees ORDER BY name')
    employees = cursor.fetchall()
    conn.close()
    return employees


def get_employee_by_id(employee_id):
    """Get a single employee by ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    return employee


def update_employee(employee_id, name, department, position):
    """Update employee details."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE employees SET name = ?, department = ?, position = ?
           WHERE id = ?''',
        (name, department, position, employee_id)
    )
    conn.commit()
    conn.close()


def delete_employee(employee_id):
    """Soft delete an employee (set is_active = 0)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE employees SET is_active = 0 WHERE id = ?', (employee_id,))
    conn.commit()
    conn.close()


def get_employees_with_encodings():
    """Get all active employees who have face encodings."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, name, face_encoding FROM employees WHERE is_active = 1 AND face_encoding IS NOT NULL'
    )
    employees = cursor.fetchall()
    conn.close()
    return employees


# ─── Attendance Operations ───────────────────────────────────────────────

def check_in(employee_id):
    """Record a check-in for an employee."""
    today = date.today().isoformat()
    now = datetime.now()

    conn = get_db()
    cursor = conn.cursor()

    # Check if already checked in today
    cursor.execute(
        'SELECT * FROM attendance WHERE employee_id = ? AND date = ?',
        (employee_id, today)
    )
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return {'success': False, 'message': 'Already checked in today', 'record': dict(existing)}

    # Determine status based on time (8:00 AM cutoff)
    status = 'present'
    if now.hour > 8 or (now.hour == 8 and now.minute > 0):
        status = 'late'

    cursor.execute(
        '''INSERT INTO attendance (employee_id, check_in_time, date, status)
           VALUES (?, ?, ?, ?)''',
        (employee_id, now.isoformat(), today, status)
    )
    record_id = cursor.lastrowid
    conn.commit()

    cursor.execute('SELECT * FROM attendance WHERE id = ?', (record_id,))
    record = cursor.fetchone()
    conn.close()

    return {'success': True, 'message': 'Checked in successfully', 'record': dict(record)}


def check_out(employee_id):
    """Record a check-out for an employee."""
    today = date.today().isoformat()
    now = datetime.now()

    conn = get_db()
    cursor = conn.cursor()

    # Find today's check-in record
    cursor.execute(
        'SELECT * FROM attendance WHERE employee_id = ? AND date = ? AND check_out_time IS NULL',
        (employee_id, today)
    )
    existing = cursor.fetchone()

    if not existing:
        conn.close()
        return {'success': False, 'message': 'No check-in record found for today'}

    cursor.execute(
        'UPDATE attendance SET check_out_time = ? WHERE id = ?',
        (now.isoformat(), existing['id'])
    )
    conn.commit()

    cursor.execute('SELECT * FROM attendance WHERE id = ?', (existing['id'],))
    record = cursor.fetchone()
    conn.close()

    return {'success': True, 'message': 'Checked out successfully', 'record': dict(record)}


def get_today_attendance():
    """Get all attendance records for today."""
    today = date.today().isoformat()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, e.name, e.department, e.position, e.photo_path
        FROM attendance a
        JOIN employees e ON a.employee_id = e.id
        WHERE a.date = ?
        ORDER BY a.check_in_time DESC
    ''', (today,))
    records = cursor.fetchall()
    conn.close()
    return records


def get_attendance_by_date_range(start_date, end_date):
    """Get attendance records within a date range."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, e.name, e.department, e.position
        FROM attendance a
        JOIN employees e ON a.employee_id = e.id
        WHERE a.date BETWEEN ? AND ?
        ORDER BY a.date DESC, a.check_in_time DESC
    ''', (start_date, end_date))
    records = cursor.fetchall()
    conn.close()
    return records


def get_employee_attendance(employee_id, start_date=None, end_date=None):
    """Get attendance records for a specific employee."""
    conn = get_db()
    cursor = conn.cursor()
    if start_date and end_date:
        cursor.execute('''
            SELECT a.*, e.name, e.department
            FROM attendance a
            JOIN employees e ON a.employee_id = e.id
            WHERE a.employee_id = ? AND a.date BETWEEN ? AND ?
            ORDER BY a.date DESC
        ''', (employee_id, start_date, end_date))
    else:
        cursor.execute('''
            SELECT a.*, e.name, e.department
            FROM attendance a
            JOIN employees e ON a.employee_id = e.id
            WHERE a.employee_id = ?
            ORDER BY a.date DESC
            LIMIT 30
        ''', (employee_id,))
    records = cursor.fetchall()
    conn.close()
    return records


def get_today_stats():
    """Get today's attendance statistics."""
    today = date.today().isoformat()
    conn = get_db()
    cursor = conn.cursor()

    # Total active employees
    cursor.execute('SELECT COUNT(*) as count FROM employees WHERE is_active = 1')
    total_employees = cursor.fetchone()['count']

    # Present today
    cursor.execute('SELECT COUNT(*) as count FROM attendance WHERE date = ?', (today,))
    present_today = cursor.fetchone()['count']

    # Late today
    cursor.execute(
        "SELECT COUNT(*) as count FROM attendance WHERE date = ? AND status = 'late'",
        (today,)
    )
    late_today = cursor.fetchone()['count']

    # Checked out
    cursor.execute(
        'SELECT COUNT(*) as count FROM attendance WHERE date = ? AND check_out_time IS NOT NULL',
        (today,)
    )
    checked_out = cursor.fetchone()['count']

    # Absent
    absent_today = total_employees - present_today

    conn.close()
    return {
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': max(0, absent_today),
        'late_today': late_today,
        'checked_out': checked_out,
        'on_time': present_today - late_today
    }


def get_weekly_stats():
    """Get attendance stats for the last 7 days."""
    from datetime import timedelta
    conn = get_db()
    cursor = conn.cursor()

    stats = []
    for i in range(6, -1, -1):
        d = (date.today() - timedelta(days=i)).isoformat()
        cursor.execute('SELECT COUNT(*) as count FROM attendance WHERE date = ?', (d,))
        present = cursor.fetchone()['count']
        cursor.execute(
            "SELECT COUNT(*) as count FROM attendance WHERE date = ? AND status = 'late'",
            (d,)
        )
        late = cursor.fetchone()['count']
        stats.append({
            'date': d,
            'present': present,
            'late': late,
            'on_time': present - late
        })

    conn.close()
    return stats


def get_employee_check_status(employee_id):
    """Get the current check-in/check-out status for an employee today."""
    today = date.today().isoformat()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM attendance WHERE employee_id = ? AND date = ?',
        (employee_id, today)
    )
    record = cursor.fetchone()
    conn.close()

    if not record:
        return 'not_checked_in'
    elif record['check_out_time'] is None:
        return 'checked_in'
    else:
        return 'checked_out'
