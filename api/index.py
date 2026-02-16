from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# --- CONFIGURATION ---
# We get the token from Vercel's secure environment variables
BOT_TOKEN = os.environ.get("TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Format: { Topic_ID: [Allowed_User_IDs] }
PERMISSIONS = {
    # Example: Topic 44 is only for User 111 and 222
    44: [111222333, 999888777],
    
    # Example: Topic 2 is only for User 555
    2: [55555555]
}

def delete_message(chat_id, message_id):
    """Sends a request to Telegram to delete the message."""
    url = f"{BASE_URL}/deleteMessage"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    requests.post(url, json=payload)

@app.route('/api/index', methods=['POST'])
def webhook():
    try:
        data = request.json
        
        # Check if the update is a message
        if "message" in data:
            msg = data["message"]
            chat_id = msg.get("chat", {}).get("id")
            message_id = msg.get("message_id")
            user_id = msg.get("from", {}).get("id")
            
            # Check for Topic ID (is_topic_message or message_thread_id)
            # In Telegram API, 'message_thread_id' is the Topic ID.
            topic_id = msg.get("message_thread_id")

            # LOGIC: If message is in a restricted topic
            if topic_id and topic_id in PERMISSIONS:
                # If user is NOT in the allowed list
                if user_id not in PERMISSIONS[topic_id]:
                    print(f"Deleting message from {user_id} in topic {topic_id}")
                    delete_message(chat_id, message_id)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

# Vercel requires this for the serverless function to run
if __name__ == '__main__':
    app.run()

