"""
Face recognition utilities for AI Employee Check-in/Check-out System.
Handles face detection, encoding, comparison, and webcam streaming.
"""

import face_recognition
import cv2
import numpy as np
import pickle
import os
from database import get_employees_with_encodings


class FaceRecognizer:
    """Manages face recognition operations."""

    def __init__(self, tolerance=0.5):
        self.known_face_encodings = []
        self.known_face_ids = []
        self.known_face_names = []
        self.tolerance = tolerance
        self.load_known_faces()

    def load_known_faces(self):
        """Load all known face encodings from the database."""
        self.known_face_encodings = []
        self.known_face_ids = []
        self.known_face_names = []

        employees = get_employees_with_encodings()
        for emp in employees:
            if emp['face_encoding']:
                try:
                    encoding = pickle.loads(emp['face_encoding'])
                    self.known_face_encodings.append(encoding)
                    self.known_face_ids.append(emp['id'])
                    self.known_face_names.append(emp['name'])
                except Exception as e:
                    print(f"Error loading encoding for employee {emp['id']}: {e}")

        print(f"Loaded {len(self.known_face_encodings)} face encodings")

    def encode_face(self, image):
        """
        Encode a face from an image (numpy array in RGB format).
        Returns the encoding or None if no face found.
        """
        face_locations = face_recognition.face_locations(image)
        if not face_locations:
            return None

        encodings = face_recognition.face_encodings(image, face_locations)
        if encodings:
            return encodings[0]
        return None

    def encode_face_from_file(self, image_path):
        """Encode a face from an image file."""
        image = face_recognition.load_image_file(image_path)
        return self.encode_face(image)

    def recognize_faces(self, frame):
        """
        Detect and recognize faces in a video frame.
        Returns list of (name, employee_id, location) tuples.
        """
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        results = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            name = "Unknown"
            employee_id = None
            confidence = 0.0

            if self.known_face_encodings:
                # Compare against known faces
                distances = face_recognition.face_distance(
                    self.known_face_encodings, face_encoding
                )
                best_match_index = np.argmin(distances)

                if distances[best_match_index] < self.tolerance:
                    name = self.known_face_names[best_match_index]
                    employee_id = self.known_face_ids[best_match_index]
                    confidence = 1.0 - distances[best_match_index]

            # Scale back face location
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            results.append({
                'name': name,
                'employee_id': employee_id,
                'location': (top, right, bottom, left),
                'confidence': round(confidence * 100, 1)
            })

        return results

    def annotate_frame(self, frame, results):
        """Draw bounding boxes and names on the frame."""
        for result in results:
            top, right, bottom, left = result['location']
            name = result['name']
            confidence = result['confidence']

            if result['employee_id']:
                # Known employee — green
                color = (0, 200, 100)
                label = f"{name} ({confidence}%)"
            else:
                # Unknown — red
                color = (0, 0, 230)
                label = "Unknown"

            # Draw bounding box
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw label background
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)[0]
            cv2.rectangle(
                frame,
                (left, bottom),
                (left + label_size[0] + 10, bottom + label_size[1] + 16),
                color,
                cv2.FILLED
            )

            # Draw label text
            cv2.putText(
                frame, label,
                (left + 5, bottom + label_size[1] + 8),
                cv2.FONT_HERSHEY_DUPLEX, 0.6,
                (255, 255, 255), 1
            )

        return frame


def encode_face_from_base64(base64_data):
    """
    Decode a base64 image and extract face encoding.
    Used for webcam capture from the browser.
    """
    import base64

    # Remove data URL prefix if present
    if ',' in base64_data:
        base64_data = base64_data.split(',')[1]

    # Decode base64 to bytes
    image_bytes = base64.b64decode(base64_data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        return None, None

    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect and encode
    face_locations = face_recognition.face_locations(rgb_image)
    if not face_locations:
        return None, None

    encodings = face_recognition.face_encodings(rgb_image, face_locations)
    if encodings:
        return encodings[0], image
    return None, None


def save_face_image(image, employee_id, save_dir='known_faces'):
    """Save a face image to disk."""
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, f"employee_{employee_id}.jpg")
    cv2.imwrite(filepath, image)
    return filepath
