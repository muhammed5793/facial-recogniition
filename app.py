
    # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process



import os
from flask import Flask, render_template, request, redirect, jsonify
import subprocess
from train import train_ai
from main2 import detect_faces_and_notify
import sqlite3
import sys
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS students (
        ad_no INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        mark REAL,
        attendance REAL,
        department TEXT
    );
    '''
    cursor.execute(create_table_query)    
    conn.commit()
    conn.close()

init_db()




app = Flask(__name__)

def get_all_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

@app.route('/')
def home():
    students = get_all_students()
    return render_template('index.html', students=students)


@app.route('/set_student_name', methods=['POST'])
def set_student_name():
    global student_name
    student_name = request.form['name']
    return "Student name set successfully!"

@app.route('/capture_feed')
def capture_feed():
    global student_name
    if student_name:
        subprocess.Popen([sys.executable, "wecam.py", student_name])
        return redirect('/')
    else:
        return "Student name is not set", 400
# def capture_feed():
#     if student_name:  # Pass the student name to the script if available
        
#         subprocess.run(["python", "wecam.py", student_name])  # Modify wecam.py to accept student name
#         return redirect('/')
#     else:
#         return "Student name is not set", 400


@app.route('/train_model')
def train_model():
    train_ai()
    return redirect('/')

@app.route('/face_detection')
def face_detection():
    if os.path.exists('model.h5'):
        detect_faces_and_notify()
    else:
        print("⚠ Model not found! Train the model first.")
    return redirect('/')

@app.route('/add_student', methods=['POST'])
def add_student():
    Ad_no = request.form['ad_no']
    name = request.form['name']
    mark = request.form['marks']
    attendance = request.form['attendance']
    department = request.form['department']
   

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO students (ad_no, name, mark, attendance, department) VALUES (?, ?, ?, ?, ?)''', (Ad_no, name, mark, attendance, department))
    conn.commit()
    conn.close()
    return redirect('/')




@app.route('/delete_student/<int:ad_no>', methods=['DELETE'])
def delete_student(ad_no):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE ad_no=?", (ad_no,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student Deleted Successfully!"})
if __name__ == '__main__':
    app.run(debug=True)