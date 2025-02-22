import requests
import json
from app.lead_finder import find_leads
from dotenv import load_dotenv

load_dotenv()

PIPEDRIVE_LEADS_URL = "https://telex.pipedrive.com/api/v1/leads"
PIPEDRIVE_NOTES_URL = "https://telex.pipedrive.com/api/v1/notes"
PIPEDRIVE_PERSONS_URL = "https://telex.pipedrive.com/api/v1/persons"

# Function to create a new person
def create_person(name, pipedrive_api_key):
    person_data = {"name": name, "visible_to": 3}
    response = requests.post(f"{PIPEDRIVE_PERSONS_URL}?api_token={pipedrive_api_key}", json=person_data)
    
    if response.status_code in [200, 201]:
        person_info = response.json().get("data", {})
        return person_info.get("id")
    else:
        print("Error creating person:", response.json())
        return None

def push_to_pipedrive(leads, pipedrive_api_key):
    responses = []
    person_id = create_person("Auto-generated Person", pipedrive_api_key)

    if not person_id:
        return [{"error": True, "message": "Could not find or create person."}]
    
    for lead in leads:
        if not isinstance(lead, dict):  # Ensure lead is a dictionary
            continue
        
        lead_data = {
            "title": f"Lead: {lead.get('name', 'Unknown')}",
            "person_id": person_id,
            "visible_to": "3"
        }
        
        lead_response = requests.post(f"{PIPEDRIVE_LEADS_URL}?api_token={pipedrive_api_key}", json=lead_data)
        
        if lead_response.status_code == 201:  # Lead created successfully
            lead_info = lead_response.json().get("data", {})
            lead_id = lead_info.get("id")

            if lead_id:
                # Add a note to the created lead
                note_data = {
                    "content": f"LinkedIn Profile: {lead.get('profile_link', '')}\n\nDetails: {lead.get('details', '')}",
                    "lead_id": lead_id
                }
                
                note_response = requests.post(f"{PIPEDRIVE_NOTES_URL}?api_token={pipedrive_api_key}", json=note_data)

                responses.append({
                    "lead": lead_info,
                    "note_status": note_response.status_code,
                    "note_response": note_response.json()
                })
            else:
                responses.append({"error": True, "message": "Lead ID not found in response."})
        else:  # Handle errors
            responses.append({
                "error": True,
                "status_code": lead_response.status_code,
                "message": lead_response.text
            })
    
    return responses

if __name__ == "__main__":
    job_title = "programmer"
    location = "San Francisco"
    pipedrive_api_key = OS.getenv("PIPEDRIVE_API_KEY")

    # Get leads from lead_finder.py
    leads = find_leads(job_title, location, "your_serp_api_key_here")
    
    # Ensure leads is a Python list (not a JSON string)
    if isinstance(leads, str):  
        leads = json.loads(leads)  
    
    # Push to Pipedrive
    responses = push_to_pipedrive(leads, pipedrive_api_key)
    
    print(json.dumps(responses, indent=4))
