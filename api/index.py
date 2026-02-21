from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

PERMISSIONS = {
    7: [5050547453,6498117062,7392546029,8458217011,5510691207],
    9: [6742391378, 5864000085, 7204020177, 5764453312, 5410200392, 7525082029,6498117062,7392546029,8458217011,5510691207],
    11: [1153233712, 5179778511, 6317547913,6498117062,7392546029,8458217011,5510691207],
    66: [1153233712,6742391378,5864000085,6633997274,6590614892,5410200392,7525082029,6498117062,7392546029,8458217011,5510691207]
}

def delete_message(chat_id, message_id):
    url = f"{BASE_URL}/deleteMessage"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    requests.post(url, json=payload)

@app.route('/api/index', methods=['POST'])
def index():
    try:
        data = request.json
        if "message" in data:
            msg = data["message"]
            chat_id = msg.get("chat", {}).get("id")
            message_id = msg.get("message_id")
            user_id = msg.get("from", {}).get("id")
            topic_id = msg.get("message_thread_id")

            if topic_id and topic_id in PERMISSIONS:
                if user_id not in PERMISSIONS[topic_id]:
                    delete_message(chat_id, message_id)

        return jsonify({"status": "ok"}), 200

    except Exception:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run()





