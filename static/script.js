function showStudentNameForm() {
    document.getElementById('student_name_prompt').style.display = 'block';
}

// Function to start webcam
function startWebcam() {
    const studentName = document.getElementById('student_name').value;
    if (studentName) {
        // Send student name to the backend via a POST request
        fetch('/set_student_name', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                name: studentName
            })
        })
        .then(response => response.ok ? response.text() : Promise.reject(response.statusText))
        .then(data => {
            document.getElementById('webcam_feed').innerHTML = "<p>Webcam started for capturing photos!</p>";
            document.getElementById('student_name_prompt').style.display = 'none';
            // Start webcam feed
            fetch('/capture_feed')
                .then(response => response.ok ? response.text() : Promise.reject(response.statusText))
                .catch(error => console.error('Error starting webcam:', error));
        })
        .catch(error => console.error('Error submitting student name:', error));
    } else {
        alert("Student name is required!");
    }
}

function trainModel() {
    fetch('/train_model')
        .then(response => response.ok ? response.text() : Promise.reject(response.statusText))
        .then(data => {
            document.getElementById('train').innerHTML += "<p>Training started! Please wait...</p>";
        })
        .catch(error => console.error('Error starting training:', error));
}

function startFaceDetection() {
    fetch('/face_detection')
        .then(response => response.ok ? response.text() : Promise.reject(response.statusText))
        .then(data => {
            document.getElementById('facedetection').innerHTML = "<p>Face detection started!</p>";
        })
        .catch(error => console.error('Error starting Detection:', error));
}


function deleteStudent(ad_no) {
    if (confirm("Are you sure you want to delete this student?")) {
        fetch(`/delete_student/${ad_no}`, { method: 'DELETE' })
        .then(response => response.json())  // Handle JSON response
        .then(data => {
            alert(data.message || "Student Deleted Successfully!");
            document.getElementById(`student-${ad_no}`).remove(); // Remove from UI instead of full reload
        })
        .catch(error => console.error('Error deleting student:', error));
    }


}
// function fetchDetectedStudent() {
//     fetch('/get_detected_student')
//         .then(response => response.json())
//         .then(data => {
//             if (data.error) {
//                 alert("No student detected!");
//             } else {
//                 document.getElementById("student_name").innerText = data.name;
//                 document.getElementById("student_adno").innerText = data.ad_no;
//                 document.getElementById("student_marks").innerText = data.marks;
//                 document.getElementById("student_attendance").innerText = data.attendance;
//                 document.getElementById("student_department").innerText = data.department;
//             }
//         })
//         .catch(error => console.error('Error fetching student data:', error));
// }
//-------------------------------
// function showStudentNameForm() {
//     document.getElementById('student_name_prompt').style.display = 'block';
// }

// // Function to start webcam
// function startWebcam() {
//     const studentName = document.getElementById('student_name').value;
//     if (studentName) {
//         // Send student name to the backend via a POST request
//         fetch('/set_student_name', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
//             body: new URLSearchParams({
//                 name: studentName
//             })
//         })
//         .then(response => response.ok ? response.text() : Promise.reject(response.statusText))
//         .then(data => {
//             document.getElementById('webcam_feed').innerHTML = "<p>Webcam started for capturing photos!</p>";
//             document.getElementById('student_name_prompt').style.display = 'none';
//             // Start webcam feed
//             fetch('/capture_feed')
//                 .then(response => response.ok ? response.text() : Promise.reject(response.statusText))
//                 .catch(error => console.error('Error starting webcam:', error));
//         })
//         .catch(error => console.error('Error submitting student name:', error));
//     } else {
//         alert("Student name is required!");
//     }
// }

// function trainModel() {
//     fetch('/train_model')
//         .then(response => response.ok ? response.text() : Promise.reject(response.statusText))
//         .then(data => {
//             document.getElementById('train').innerHTML += "<p>Training started! Please wait...</p>";
//         })
//         .catch(error => console.error('Error starting training:', error));
// }

// function startFaceDetection() {
//     fetch('/face_detection')
//         .then(response => response.ok ? response.text() : Promise.reject(response.statusText))
//         .then(data => {
//             document.getElementById('facedetection').innerHTML = "<p>Face detection started!</p>";
//         })
//         .catch(error => console.error('Error starting Detection:', error));
// }


// function deleteStudent(ad_no) {
//     if (confirm("Are you sure you want to delete this student?")) {
//         fetch(/delete_student/${ad_no}, { method: 'DELETE' })
//         .then(response => response.json())  // Handle JSON response
//         .then(data => {
//             alert(data.message || "Student Deleted Successfully!");
//             document.getElementById(student-${ad_no}).remove(); // Remove from UI instead of full reload
//         })
//         .catch(error => console.error('Error deleting student:', error));
//     }


// }
