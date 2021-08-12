from dotenv import load_dotenv
from flask import *
from flask_socketio import *
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

load_dotenv()

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
def call(message):

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    try:
        client.calls.create(
            method='GET',
            url='http://demo.twilio.com/docs/voice.xml',
            status_callback_method='POST',
            status_callback=os.getenv('STATUS_CALLBACK'),
            status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
            to=message['data'],
            from_=os.getenv('TWILIO_FROM_PHONE')
        )
    except TwilioRestException:
        print("Unable to create record")
        socketIo.emit('invalidNumber', {'data': message['data']})

@app.route('/')
def hello():
    return "Hello World"

@app.route('/voice', methods=['POST'])
def voice():
    data = request.values['CallStatus']
    socketIo.emit('callStatus', {'data': data}, broadcast=True)
    return data
if __name__ == '__main__':
    socketIo.run(app)




