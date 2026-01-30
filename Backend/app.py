from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus


app = Flask(__name__)
CORS(app)

# 🔐 Load environment variables
load_dotenv()

# 🔐 Read & encode password
raw_password = os.getenv("MONGO_PASSWORD")
password = quote_plus(raw_password)

# 🔗 MongoDB connection
client = MongoClient(
    f"mongodb+srv://choudharyvaishali393_db_user:{password}@cluster0.gihk3y9.mongodb.net/?appName=Cluster0"
)

db = client["techstax"]
collection = db["events"]

def format_message(data):
    author = data.get("sender", {}).get("login", "Unknown")
    time = datetime.utcnow().strftime("%d %b %Y - %I:%M %p UTC")

    if "ref" in data:
        branch = data["ref"].split("/")[-1]
        return f'"{author}" pushed to "{branch}" on {time}'

    if "pull_request" in data and data.get("action") != "closed":
        from_branch = data["pull_request"]["head"]["ref"]
        to_branch = data["pull_request"]["base"]["ref"]
        return f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {time}'

    if data.get("action") == "closed" and data.get("pull_request", {}).get("merged"):
        from_branch = data["pull_request"]["head"]["ref"]
        to_branch = data["pull_request"]["base"]["ref"]
        return f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {time}'

    return f'Unknown action by "{author}" on {time}'


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = format_message(data)

    collection.insert_one({
        "message": message,
        "timestamp": datetime.utcnow()
    })

    return jsonify({"status": "saved"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    try:

        events = list(collection.find({}, {"_id": 0}))
        return jsonify(events)
    except Exception as e:
        print("🔥 ERROR IN /events 🔥")
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
 

    app.run(port=5000)
