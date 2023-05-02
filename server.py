import socket
import socketio
from waitress import serve
from livevideo import app

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
sio = socketio.Server()
app_server = socketio.WSGIApp(sio, app)

if __name__ == '__main__':
    print(f'Server started, connect with http://127.0.0.1:8080 or http://{ip_address}:8080')
    serve(app_server, host='0.0.0.0', port=8080, url_scheme='http', threads=4)