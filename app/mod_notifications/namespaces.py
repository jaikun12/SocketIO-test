import eventlet
eventlet.patcher.monkey_patch()
from flask import current_app, request
from flask_socketio import SocketIO, emit, Namespace
from threading import Lock

thread = None

def background_thread(socket_instance, request_sid):
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        # socket_instance.sleep(5)
        count += 1
        socket_instance.emit('response', {'data': 'Server generated event'}, namespace='/notification', room=request_sid)
        socket_instance.sleep(5)



class NotificationNameSpace(Namespace):
    __namespace__ = "notification"
    response_tag = "notification"

    def on_connect(self):
        from app import socketio
        global thread
        emit("connected", "connected")
        socketio.sleep(5)
        if thread is None:
            with current_app.app_context():
                thread = socketio.start_background_task(background_thread, socketio, request.sid)



