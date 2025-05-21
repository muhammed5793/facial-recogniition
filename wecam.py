import cv2
import os
import uuid
import sys

def capture_feed(student_name):  # Accept student name as a parameter
    print(f"Starting image capture for {student_name}...")
    haar_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(haar_cascade_path)

    # Input for base directory and student name
    # dataset_dir = input("Enter the base directory for storing datasets (e.g., 'data/'): ")
    dataset_dir = './data'
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    student_training_dir = os.path.join(dataset_dir, f"training/{student_name}")
    student_validation_dir = os.path.join(dataset_dir, f"validation/{student_name}")

    os.makedirs(student_training_dir, exist_ok=True)
    os.makedirs(student_validation_dir, exist_ok=True)

    video_capture = cv2.VideoCapture(0)
    capture_limit = 100
    captured_count = 0

    print("Press 'C' to capture an image. Press 'Q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display the video feed
        cv2.imshow("Capture Images", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c') and len(faces) > 0:  # Capture an image when 'C' is pressed
            for (x, y, w, h) in faces:
                cropped_face = gray_frame[y:y + h, x:x + w]
                file_name = f"face_{uuid.uuid4().hex}.jpg"

                if captured_count < int(capture_limit * 1.6):
                    cv2.imwrite(os.path.join(student_training_dir, file_name), cropped_face)
                else:
                    cv2.imwrite(os.path.join(student_validation_dir, file_name), cropped_face)

                captured_count += 1
                print(f"Captured {captured_count}/{capture_limit}")
                
                # Break if the limit is reached
                if captured_count >= 200:
                    video_capture.release()
                    cv2.destroyAllWindows()

        elif key == ord('q'):  # Quit when 'Q' is pressed
            print("Exiting image capture...")
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print(f"Images saved in {dataset_dir}")

# Run the function
if __name__ == "__main__":
    if len(sys.argv) > 1:
        student_name = sys.argv[1]  # Retrieve student name from command-line argument
        capture_feed(student_name)
