from flask import Flask, request, json
import logging
import os
import gpt_api
import facebook_response

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Path to the message log file
LOG_FILE = r'C:\Users\admin\Facebook bot\message_log.json'
PROMPT_FILE = r'C:\Users\admin\Facebook bot\recipient_prompt.json'

@app.route('/webhook', methods=['GET'])
def verify():
    # Verification endpoint to confirm webhook setup with Facebook
    verify_token = 'abc'
    logging.info("Received GET request for verification")
    try:
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if request.args.get("hub.verify_token") == verify_token:
                logging.info("Verification successful")
                return request.args["hub.challenge"], 200
            logging.warning("Verification token mismatch")
            return "Verification token mismatch", 403
        return "Hello world", 200
    except Exception as e:
        logging.error("Error during verification: %s", e)
        return "Internal server error", 500

def is_valid_json_structure(data):
    """Validate the structure of the received JSON data."""
    try:
        # Check if the required fields are present and correctly structured
        if "object" in data and data["object"] == "page":
            entries = data.get("entry", [])
            if isinstance(entries, list) and entries:
                for entry in entries:
                    if "id" in entry and "messaging" in entry and isinstance(entry["messaging"], list):
                        for message in entry["messaging"]:
                            if all(key in message for key in ("sender", "recipient", "message", "timestamp")):
                                return True
        return False
    except KeyError:
        return False

def save_to_log(data, response):
    sender_id = data["entry"][0]["messaging"][0]["sender"]["id"]  # Extract sender_id
    message = data["entry"][0]["messaging"][0]["message"]          # Extract message data
    timestamp = data["entry"][0]["messaging"][0]["timestamp"]      # Extract message timestamp
    time = data["entry"][0]["time"]                                # Extract entry time

    # Get the message text directly without decoding
    if "text" in message:
        message_text = message["text"]
    else:
        message_text = None  # Handle case where there is no text

    # Directly assign the response without encoding/decoding
    response_text = response

    # Structure of the message to be saved
    message_data = {
        "message": message_text,
        "response": response_text,
        "timestamp": timestamp,
        "entry_time": time
    }

    # Ensure the log file exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)  # Create an empty dict in the file if it doesn't exist

    # Open the log file and update it with new data
    with open(LOG_FILE, 'r+', encoding='utf-8') as f:
        # Read the existing data
        file_data = json.load(f)

        # If the sender_id already exists, append the new message to the list
        if sender_id in file_data:
            file_data[sender_id].append(message_data)
        else:
            # If sender_id doesn't exist, create a new entry for this sender
            file_data[sender_id] = [message_data]

        # Move the file pointer to the beginning to overwrite
        f.seek(0)
        json.dump(file_data, f, indent=2, ensure_ascii=False)  # Ensure non-ASCII characters are preserved

    logging.info("Data saved successfully for sender_id: %s", sender_id)

def get_chat_history(LOG_FILE, recipient_id):
    with open(LOG_FILE, 'r+', encoding='utf-8') as f:
            conversation_history = json.load(f)
    history = conversation_history.get(recipient_id, [])
    history_messages = []

    # Construct the history messages
    for entry in history:
        if entry['message'] is not None:  # Only include non-null messages
            history_messages.append(f"User: {entry['message']}")
            history_messages.append(f"GPT: {entry['response']}")

    # Join the history into a single string
    history_text = "\n".join(history_messages)
    return history_text

@app.route('/webhook', methods=['POST'])
def webhook():
    # Handle incoming messages
    logging.info("Received POST request with event data")
    try:
        data = request.get_json()
        logging.info("POST Request Data: %s", json.dumps(data, indent=2))

        # Save the received data to message_log.json
        if is_valid_json_structure(data) and data["entry"][0]["messaging"][0]["sender"]["id"] != 8176163065778443:
            logging.warning("Valid JSON structure, save data")
            
            # 1. Get id and message of recipient 
            message = data["entry"][0]["messaging"][0]["message"]  
            recipient_id = data["entry"][0]["messaging"][0]["sender"]["id"]

            # 2. Get the reponse to the mesage from gpt api, add extra prompt
            with open(PROMPT_FILE, 'r+', encoding='utf-8') as f:
                recipient_prompt = json.load(f)
            try:
                extra_prompt = recipient_prompt[str(recipient_id)]['prompt']
            except:
                extra_prompt = ""

            # 3. Get the conversation history
            try:
                with open(LOG_FILE, 'r+', encoding='utf-8') as f:
                    conversation_history = json.load(f)
                history = conversation_history.get(recipient_id, [])
                history_messages = []
        
                # Construct the history messages
                for entry in history:
                    if entry['message'] is not None:  # Only include non-null messages
                        history_messages.append(f"User: {entry['message']}")
                        history_messages.append(f"GPT: {entry['response']}")

                # Join the history into a single string
                history_text = "\n".join(history_messages)
            except:
                history_text = ""

            response = gpt_api.chat_gpt(message, extra_prompt, history_text)

            # 4. Send the response from gpt via facebook
            facebook_response.send_message(recipient_id, response)

            save_to_log(data, response)
            print(response)
            # print(history_text)
        else:
            logging.warning("Invalid JSON structure, data not saved")
        
        return "Event received", 200
    except Exception as e:
        logging.error("Error processing event: %s", e)
        return "Internal server error", 500

            
if __name__ == '__main__':
    app.run(port=6000, debug=True)

