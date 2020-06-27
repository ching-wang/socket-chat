from markupsafe import escape
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import logging
import coloredlogs
import sys
import datetime
from collections import deque, namedtuple
import uuid


app = Flask(__name__)
coloredlogs.install()
# handler = logging.StreamHandler(sys.stdout)
# app.logger.addHandler(handler)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app, logger=False)

ChatMessage = namedtuple(
    "ChatMessage", ["message", "sender", "time", "msg_id"])

channelLists = {'First Channel': deque([], 10)}


# show the home page
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

# Display name Login
@app.route("/login", methods=["POST"])
def login():
    session.clear()
    # save display name in session
    session['display_name'] = request.form.get("display_name")
    # render a template showing list of chats and form to create new one

    # Flash message to show login in successfully
    flash('login successfully. Please create a channel or join one to start t chart', 'success')
    return redirect('/main')


@app.route("/main", methods=["GET"])
def main():
    return render_template('main.html', channels=channelLists)

    # logout

    # @app.route("/logout", methods=["GET"])
    # def logout():
    #     session.clear()
    #     flash('You are successfully logged out. Please create a channel or join one to start t chart', 'success')
    #     return render_template("index.html")


@socketio.on('connect')
def test_connect():
    emit('confirm_connected', {"Connected": True})


@socketio.on("join_channel")
def on_join_channel(data):
    logging.warn("join_channel %s", data)
    channel_name = data["channelName"]

    if channel_name not in channelLists:
        channelLists[channel_name] = deque([], 10)
        emit("new_channel_created", {
             "channel": channel_name}, broadcast=True)
        emit(
            'server_msg',
            {
                'msg': f"New channel {channel_name} has been created by {session['display_name']}",
            },
            broadcast=True)

    join_room(channel_name)
    emit("joined_channel", {"channelName": channel_name})

    if 'channel_name' in session and session['channel_name'] == channel_name:
        pass
    else:
        logging.warn("User joining channel %s %s",
                     session['display_name'], channel_name)
        for chat_message in channelLists[channel_name]:
            logging.warn(
                "Re-sending old chat message to new channel joiner: %s", chat_message)
            emit(
                "chat_msg",
                {
                    "msg": chat_message.message,
                    "from": chat_message.sender,
                    "created_at": chat_message.time,
                    "msg_id": chat_message.msg_id})
        logging.warn("Announcing joining user in channel %s %s",
                     session['display_name'], channel_name)
        emit(
            "server_msg",
            {
                "msg": f"{session['display_name']} has joined the {channel_name} channel"
            },
            room=channel_name)
    session['channel_name'] = data["channelName"]


@socketio.on("leave")
def on_leave(data):
    logging.info("leave %s", data)
    username = session['display_name']
    channel_name = data["channelName"]
    leave_room(channel_name)
    emit("left_channel", {"channel": channel_name})
    emit(
        "server_msg",
        {
            "msg": f"{username} has left the {channel_name} channel."
        },
        room=channel_name
    )


@socketio.on("send_chat_msg")
def on_send_chat_msg(data):
    logging.info("chat_msg %s", data)
    channel_name = data["channelName"]
    if data["msg"] and channel_name:
        chat_message = ChatMessage(
            message=data["msg"],
            sender=session["display_name"],
            time=datetime.datetime.now().replace(microsecond=0).isoformat(),
            msg_id=uuid.uuid4().hex)
        channelLists[channel_name].append(chat_message)
        emit(
            "chat_msg",
            {
                "msg": chat_message.message,
                "from": chat_message.sender,
                "created_at": chat_message.time,
                "msg_id": chat_message.msg_id
            },
            room=data["channelName"])
# private message
# @socketio.on('private_message')
# def private_message(private_message):

#     print(private_message)
# delete ones message


@socketio.on("delete_message")
def on_delete_msg(data):
    logging.info("on_delete_msg %s", data)
    # Find and delete this message in the deque.

    emit(
        "message_deleted",
        {
            "msg_id": data.msg_id
        },
        broadcast=True)

# Receiving message
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    socketio.run(app)
