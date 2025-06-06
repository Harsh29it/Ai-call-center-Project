from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)
# for connecting the call 
@app.route("/voice", methods=['POST'])
def voice():
    print(">>> /voice hit")
    resp = VoiceResponse()
    gather = resp.gather(input='speech', action='/name', timeout=5)
    gather.say("Welcome to the AI Call Center. Please say your name.")
    return str(resp)

# asking name 
@app.route("/name", methods=['POST'])
def name():
    name = request.form.get('SpeechResult')
    print(">>> /name hit | User said name:", name)

    resp = VoiceResponse()
    if not name:
        resp.say("Sorry, I didn't catch that. Redirecting.")
        resp.redirect('/voice')
        return str(resp)

    gather = resp.gather(input='speech', action='/age', timeout=5)
    gather.say(f"Thanks {name}. Now please say your age.")
    return str(resp)

# asking age
@app.route("/age", methods=['POST'])
def age():
    age = request.form.get('SpeechResult')
    print(">>> /age hit | User said age:", age)

    resp = VoiceResponse()
    if not age:
        resp.say("Sorry, I didn't catch that. Let's try again.")
        resp.redirect('/voice')
        return str(resp)

    resp.say("Connecting you to a human agent.")
    resp.dial("+9174668083008")  # number of the avilabe agent
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
