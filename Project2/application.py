import os, requests, string, time, datetime

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit

counter = 0 #It is used to "generate" the keys in the dictionary messages.
channels = [] #A list of all the channel names.
messages = {}
#messages = {
#    1: [(text, username, timestamp), (...), (...)]
#    2: ....
#    3: ...
#}

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template('home.html')

#this route is used when reloading a page say "localhost:port/3"
#so as not to crash. It reloads the home.html with the same route.
#The number of the channel is stored is the localStrorage of browser.
@app.route("/<int:channel_id>", methods=['GET'])
def reload(channel_id):
    return render_template("home.html")

@app.route("/getchannels", methods=['POST'])
def getchannels():
    return jsonify({"channels": channels})

#returns all messages from the choosed channel when I load the page.
@app.route("/getmessages", methods=['POST'])
def getmessages():
    channel_id = int(request.form.get("channel_id"))
    return jsonify(messages[channel_id])

#socket form channel creation
@socketio.on("submit_new_channel")
def channel_creation(data):
    new_channel_name = data["new_channel_name"]
    channels.append(new_channel_name)
    global counter
    counter += 1
    messages.update({counter: []})
    emit("announce_new_channel", {"new_channel_name": new_channel_name}, broadcast=True)

#socket for message creation
@socketio.on("submit_new_message")
def message_creation(data):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    new_message = (data["new_message_text"], data["username"], st)
    messages[data["channel_id"]].append(new_message)
    messages[data["channel_id"]] = messages[data["channel_id"]][-100:] #store the last 100 messages
    emit("announce_new_message", {"new_message": new_message, "channel_id": data["channel_id"]}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
