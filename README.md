# facial-recognition-app
assignment of distributed systems course

## denpendencies required before running the app
```
pip3 install Flask
pip3 install socketio
pip3 install Flask-SocketIO
pip3 install numpy
pip3 install opencv-python
pip3 install waitress
pip3 install cmake
pip3 install dlib
pip3 install face_recognition
```
Before installing CMake, it is necessary to install the C++ development environment. After installing the C++ development environment, please restart your computer and try "pip3 install cmake" again. If there are no issues, proceed to the next step and install dlib using the specified command.

##run the app
After entering "python server.py" in the terminal, you can view it on the port "http://127.0.0.1:8080/". If your phone or other device is on the same LAN as the host, you can also enter the other IP address shown on console to view the live streaming of the facial recognition results on another device.