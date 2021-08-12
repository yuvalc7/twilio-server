from flask import *
from twilio.rest import Client
from flask_socketio import *
from dotenv import load_dotenv
load_dotenv()
import os
app = Flask(__name__)
socketIo = SocketIO(app, cors_allowed_origins="*")

# SocketIO Events
@socketIo.on('connect')
def connected():
    print('Connected')

@socketIo.on('disconnect')
def disconnected():
    print('Disconnected')

@socketIo.on('CallPhoneNumber')
def CallPhoneNumber(message):

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        method='GET',
        url='http://demo.twilio.com/docs/voice.xml',
        status_callback_method='POST',
        status_callback='http://324cb6a24342.ngrok.io/voice',
        status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
        to=message['data'],
        from_='+16514136922'
    )
    print(call.sid)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/voice', methods=['POST'])
def voice():
    data = request.values['CallStatus']
    socketIo.emit('callStatus', {'data': data}, broadcast=True)

if __name__ == '__main__':
    socketIo.run(app)




