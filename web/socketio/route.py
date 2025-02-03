from datetime import time
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user
from web import socketio
from flask_socketio import emit, join_room, leave_room
# Predefined rooms for chat
ROOMS = ["lounge", "news", "games", "coding"]

socket_bp = Blueprint('socket_bp', __name__)

@socket_bp.route("/socket-chat", methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))

    return render_template("chat.html", username=current_user.username, rooms=ROOMS)



""" @socketio.on('incoming-msg')
def on_message(data):
    #Broadcast messages

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    socketio.send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)


@socketio.on('join')
def on_join(data):
    #User joins a room

    username = data["username"]
    room = data["room"]
    socketio.join_room(room)

    # Broadcast that new user has joined
    socketio.send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    #User leaves a room

    username = data['username']
    room = data['room']
    socketio.leave_room(room)
    socketio.send({"msg": username + " has left the room"}, room=room) """