from flask import request, jsonify, Blueprint
from app import app
from app.lead_finder import find_leads
from app.pipedrive import push_to_pipedrive
import os
import json

from dotenv import load_dotenv
load_dotenv()

#routes = Blueprint('routes', __name__)

def extract_api_keys(settings):
    """Extracts pipedrive_api_key and serp_api_key from settings array."""
    pipedrive_api_key = None
    serp_api_key = None

    for item in settings:
        if item.get("label") == "pipedrive_api_key":
            pipedrive_api_key = item.get("default")
        elif item.get("label") == "serp_api_key":
            serp_api_key = item.get("default")

    return pipedrive_api_key, serp_api_key


@app.route('/find-leads', methods=['GET'])
def get_leads():
    query = request.args.get('query')
    leads = find_leads(query)
    return jsonify(leads)

@app.route('/push-leads', methods=['POST'])
def push_leads():
    data = request.get_json()
    response = push_to_pipedrive(data)
    return jsonify(response)

@app.route("/process-message", methods=["POST"])
def process_message():
    data = request.json
    print("Received Telex Payload:", json.dumps(data, indent=4))
    message = data.get("message", "").strip()
    settings = data.get("settings", [])

    pipedrive_api_key, serp_api_key = extract_api_keys(settings)
    
    if not message or not pipedrive_api_key or not serp_api_key:
        return jsonify({"error": "Missing required parameters"}), 400


    import re
    message = re.sub(r"<.*?>", "", message).strip()        
    
    # Extract role and location from the message
    words = message.lower().split()
    if "in" in words:
        in_index = words.index("in")
        role = " ".join(words[:in_index])
        location = " ".join(words[in_index + 1:])
    else:
        return jsonify({"error": "Invalid message format. Use 'find [role] in [location]'"}), 400
    
    leads = find_leads(role, location, serp_api_key)
    
    if not leads:
        return jsonify({"message": "No leads found"}), 200
    
    push_to_pipedrive(leads, pipedrive_api_key)
    
    return jsonify({
    "event_name": "leads_found",
    "message": f"Leads have been pushed to Pipedrive. {len(leads)} leads found.",
    "status": "success",
    "username": "lead-finder-bot",
    "response_text": f"✅ Leads have been successfully pushed to Pipedrive!"
})




@app.route('/integration-json', methods=['GET'])
def get_integration_json1():
    integration1_json = {
        "data": {
            "date": {
            "created_at": "2025-02-21",
            "updated_at": "2025-02-21"
            },
            "descriptions": {
            "app_description": "Automates finding and pushing leads to the pipedrive crm.",
            "app_logo": "https://images.app.goo.gl/3fgQiWc5o11DUPrL7",
            "app_name": "Telex Lead to Pipedrive Integration",
            "app_url": "https://2409-197-211-63-96.ngrok-free.app",
            "background_color": "#ffffff"
            },
            "integration_category": "CRM & Customer Support",
            "integration_type": "output",
            "is_active": False,
            "output": [
            {
                "label": "output_channel_1",
                "value": True
            },
            {
                "label": "output_channel_2",
                "value": False
            }
            ],
            "key_features": [
            "Extracts needed lead datails from telex messages",
            "Uses google dorking to find those leads on linkedin",
            "creates a new pipedrive person",
            "Pushes those leads to the person on pipedrive crm"
            ],
            "permissions": {
            "monitoring_user": {
                "always_online": True,
                "display_name": "Performance Monitor"
            }
            },
            "settings": [
            {
                    "default": "https://yourdomain.com/push-leads",
                    "label": "target_url",
                    "required": True,
                    "type": "text"
                },
                {
                    "default": "",
                    "label": "pipedrive_api_key",
                    "description": "Your Pipedrive API key to authenticate requests.",
                    "required": True,
                    "type": "text"
                },
                {
                    "default": os.getenv("DEFAULT_SERP_API_KEY", ""),
                    "label": "serp_api_key",
                    "description": "Your SERP API key to enable lead search. Defaults to system key if not provided.",
                    "required": False,
                    "type": "text"
                }    
            ],
            "tick_url": "https://2409-197-211-63-96.ngrok-free.app/process-message",
            "target_url": "https://2409-197-211-63-96.ngrok-free.app/process-message"
        }
        }
    return jsonify(integration1_json)
        
@app.route('/integration.json', methods=['GET'])
def get_integration_json():
    integration_json = {
        "data": {
            "author": "David",
            "date": {
                "created_at": "2025-02-21",
                "updated_at": "2025-02-21"
            },
            "descriptions": {
                "app_description": "An output integration that sends leads from Telex to Pipedrive.",
                "app_logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdoccj7yhjCzd-prx5IcQyUZjCwIXCGpVByw&s",
                "app_name": "Telex to Pipedrive Sync",
                "app_url": "https://2409-197-211-63-96.ngrok-free.app",
                "background_color": "#ffffff"
            },
            "integration_category": "CRM & Customer Support",
            "integration_type": "output",
            "is_active": True,
            "key_features": [
                "Automatically push leads from Telex to Pipedrive.",
                "Create and link persons for better CRM management.",
                "Seamlessly integrate with existing workflows."
            ],
            "permissions": {
                "events": [
                    "Receive messages from Telex.",
                    "Extract and process lead details.",
                    "Push leads to Pipedrive.",
                    "Log integration activities."
                ]
            },
            "settings": [
               {
                    "default": "https://2409-197-211-63-96.ngrok-free.app",
                    "label": "target_url",
                    "required": True,
                    "type": "text"
                },
                {
                    "default": "",
                    "label": "pipedrive_api_key",
                    "description": "Your Pipedrive API key to authenticate requests.",
                    "required": True,
                    "type": "text"
                },
                {
                    "default": os.getenv("DEFAULT_SERP_API_KEY", ""),
                    "label": "serp_api_key",
                    "description": "Your SERP API key to enable lead search. Defaults to system key if not provided.",
                    "required": False,
                    "type": "text"
                }    
            ],
            "target_url": "https://2409-197-211-63-96.ngrok-free.app/process-message",
            "tick_url": "https://2409-197-211-63-96.ngrok-free.app/process-message",
            "website": "https://2409-197-211-63-96.ngrok-free.app"
        }
    }
    return jsonify(integration_json)
