import cv2
import face_recognition
import numpy as np
import os

from flask import Flask, Response, render_template
from flask_socketio import SocketIO

# Flask app
app = Flask(__name__)
socketioApp = SocketIO(app)

# Images and class names
path = "images"
classNames = os.listdir(path)
images = [cv2.imread(f"{path}/{cl}") for cl in classNames]
classNames = [os.path.splitext(cl)[0].upper() for cl in classNames]

# Function that returns a array of encodings for each image.
def findEncodings(images):
    encodeList =[]
    for img in images:
        img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Function that returns a array of encodings for each image.
encodeListKnown= findEncodings(images)
print("Encoding complete!")

# video capture 
cap = cv2.VideoCapture(0)

def gen_frames():
    frame_skip = 1  # Skip every other frame.
    count = 0  # Frame counter.
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break

        count += 1
        if count % frame_skip != 0:
            continue
        
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesInCurrentFrame = face_recognition.face_locations(imgS)  # multiple faces
        encodingsCurrentFrame = face_recognition.face_encodings(imgS, facesInCurrentFrame)

        # Loop through the faces in the current frame
        for encodeFace, face_location in zip(encodingsCurrentFrame, facesInCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
            # Match index is set to the lowest distance that is the most accurate.
            matchIndex = np.argmin(faceDist)
            # Check if index exists
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                matchPerc = round(faceDist[matchIndex] * 100)
                y1, x2, y2, x1 = [coord * 4 for coord in face_location]  # Multiply by 4 to get the original size.
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f"{name} {matchPerc}%", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            else:
                y1, x2, y2, x1 = [coord * 4 for coord in face_location]  # Multiply by 4 to get the original size.
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # encode frame as jpeg
        ret, buffer = cv2.imencode('.jpg', img)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release() #turn off camera  
    cv2.destroyAllWindows() #close all windows


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    #Video streaming Home Page
    
    return render_template('index.html')

def run():
    socketioApp.run(app)

if __name__ == '__main__':
    socketioApp.run(app)