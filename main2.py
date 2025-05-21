import os
import cv2
import sqlite3
from tensorflow.keras.models import load_model
import smtplib
from email.mime.text import MIMEText


def get_model():
    model_path = 'model.h5'
    if os.path.exists(model_path):
        return load_model(model_path)
    else:
        print("⚠ Model not found! Train the model first.")
        return None  # Return None instead of crashing

model = get_model()

def get_class_labels(training_folder):
    class_labels = sorted(os.listdir(training_folder))  # Get class labels from the dataset
    return class_labels

training_folder = 'data/training'
class_labels = get_class_labels(training_folder)



def send_email(data):
    email_address = "muhammedhariskv3@gmail.com"
    email_password = "ntjy bxqd lhqh krnp"
    
    msg = MIMEText(data)
    msg['Subject'] = "Detected Student"
    msg['From'] = email_address
    msg['To'] = "aboobackerkv598@gmail.com"

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(msg)
        print("Email sent successfully!")

def detect_faces_and_notify():
    

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml").detectMultiScale(gray)

        for (x, y, w, h) in faces:
            face = frame[y:y + h, x:x + w]
            face = cv2.resize(face, (150, 150)).reshape(1, 150, 150, 3) / 255.0

            if model is not None:
                predictions = model.predict(face)
                predicted_index = predictions.argmax()
                predicted_class = class_labels[predicted_index]
                confidence = predictions.max()
            else:
                predicted_class = "Unknown"
                confidence = 0

            if confidence < 0.6:  # Confidence threshold to detect "Stranger"
                predicted_class = "Stranger"
                confidence = 0
                student_data = None
            else:
                cursor.execute("SELECT * FROM students WHERE ad_no=?", (predicted_class,))
                student_data = cursor.fetchone()

            if student_data:
                # detected_student = {q
                #         "ad_no": student_data[0],
                #         "name": student_data[1],
                #         "marks": student_data[2],
                #         "attendance": student_data[3],
                #         "department": student_data[4]
                #     }
                # label = f"{student_data[1]} ({predicted_class}) - {confidence * 100:.2f}%"
                student_name = student_data[1]  # Extract name from database
                label = f"{student_name} ({predicted_class}) - {confidence * 100:.2f}%"
            else:
                label = f"Stranger - {confidence * 100:.2f}%"

            print(f"Detected: {label}")

            # Draw rectangle and text on frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Send email when 's' key is pressed
            if student_data and (cv2.waitKey(1) & 0xFF == ord('s')):
                data_str = f"Name: {student_data[1]}, Admission No: {student_data[0]}, Department: {student_data[4]}, Attendance: {student_data[3]}, Marks: {student_data[2]}"
                send_email(data_str)

        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    conn.close()
