import os
from flask import Flask, request
from datetime import datetime
import re
from twilio.twiml.voice_response import VoiceResponse


app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/test")
def test():
    return "Test Successful"

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

# @app.route("/callrouting")
# def call_routing():

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    callednumber = request.values['Called']
    if "2274" in callednumber:
        resp.say('Matched!', voice='alice')
    else:
        # Read a message aloud to the caller
        resp.say("Thank you for calling! Have a great day.", voice='alice')

    return str(resp)

# @app.route("/voice", methods=['GET', 'POST'])
# def voice():
#     """Respond to incoming phone calls and mention the caller's city"""
#     # Get the caller's city from Twilio's request to our app
#     city = request.values['FromCity']

#     # Start our TwiML response
#     resp = VoiceResponse()

#     # Read a message aloud to the caller
#     resp.say('Never gonna give you up, {}!'.format(city), voice='alice')

#     # Play an audio file for the caller
#     resp.play('https://demo.twilio.com/docs/classic.mp3')

#     return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))