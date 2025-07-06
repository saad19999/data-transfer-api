from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Use environment variable for API Key for security
API_KEY = os.environ.get("API_KEY", "your_default_api_key_here")

# Temporary storage for the last sent data
# This will be lost if the app restarts (e.g., during deployment, scaling, or maintenance)
last_data = {"value": None, "timestamp": None}

@app.route("/send", methods=["POST"])
def send_data():
    global last_data
    
    # Authenticate with API Key
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data or "value" not in data:
        return jsonify({"error": "Invalid data format. 'value' field is required."}), 400

    last_data["value"] = data["value"]
    last_data["timestamp"] = datetime.now().isoformat()
    
    return jsonify({"message": "Data received successfully", "data": last_data["value"]}), 200

@app.route("/get", methods=["GET"])
def get_data():
    # Authenticate with API Key
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    if last_data["value"] is None:
        return jsonify({"message": "No data available yet"}), 204 # No Content
    
    return jsonify({"value": last_data["value"], "timestamp": last_data["timestamp"]}), 200

if __name__ == "__main__":
    from datetime import datetime # Import here for local testing
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))


