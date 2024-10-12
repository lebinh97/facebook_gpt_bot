from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/webhook', methods=['GET'])
def verify():
    # Verification endpoint to confirm webhook setup with Facebook
    verify_token = "YOUR_VERIFY_TOKEN"
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == verify_token:
            return request.args["hub.challenge"], 200
        return "Verification token mismatch", 403
    return "Hello world", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    # Handle incoming messages
    data = request.get_json()
    print(json.dumps(data, indent=2))
    # Process the message event here
    return "Event received", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
