import eventlet
eventlet.patcher.monkey_patch()
from threading import Lock
from flask import Flask, request
from flask_socketio import SocketIO, emit
from mod_notifications.namespaces import NotificationNameSpace

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

socketio = SocketIO(cors_allowed_origins="*", engineio_logger=True, logger=True, async_mode='eventlet')
socketio.init_app(app)
thread = None
thread_lock = Lock()


socketio.on_namespace(NotificationNameSpace('/notification'))


# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         # socket_instance.sleep(5)
#         count += 1
#         socketio.emit('response', {'data': 'Server generated event'}, namespace='/notification')
#         socketio.sleep(5)


@app.route("/")
def index():
    return "Test SocketIO"


@socketio.event
def connect():
    emit('my_response', {'data': 'Connected', 'count': 0})
    socketio.sleep(0)
    # socketio.start_background_task(background_thread)


if __name__ == '__main__':
    socketio.run(app)





