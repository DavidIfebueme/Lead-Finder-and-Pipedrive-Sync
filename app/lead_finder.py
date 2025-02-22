import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()


SERP_API_URL = "https://serpapi.com/search"

def clean_text(text):
    return re.sub(r"[^\w\s,.-]", "", text).strip()

def extract_name(full_title):
    return full_title.split(" - ")[0]  

def extract_details(description):
    """Cleans up the description and returns it as a single field."""
    return clean_text(description)

def find_leads(job_title, location, serp_api_key):  # Added serp_api_key as a parameter
    query = f'site:linkedin.com/in "{job_title}" "{location}"'
    
    params = {
        "engine": "google",
        "q": query,
        "num": 10,
        "api_key": serp_api_key  # Now using the passed API key
    }
    
    response = requests.get(SERP_API_URL, params=params)
    if response.status_code != 200:
        return {"error": "Failed to fetch data from SerpAPI"}
    
    data = response.json()
    leads = []
    
    for result in data.get("organic_results", []):
        full_title = result.get("title", "")
        description = result.get("snippet", "")

        name = extract_name(full_title)
        details = extract_details(description)

        lead = {
            "name": name,
            "profile_link": result.get("link"),
            "details": details
        }
        leads.append(lead)
    
    return leads  # Returning the list instead of JSON string

if __name__ == "__main__":
    job_title = "Sales Manager"
    location = "New York"
    serp_api_key = OS.getenv("SERP_API_KEY")
    print(find_leads(job_title, location, serp_api_key))
