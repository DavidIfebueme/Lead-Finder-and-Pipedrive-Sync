import pytest
import requests
from unittest.mock import patch
from app.lead_finder import find_leads

SERP_API_URL = "https://serpapi.com/search"

# Mock responses
MOCK_SUCCESS_RESPONSE = {
    "organic_results": [
        {
            "title": "John Doe - Software Engineer",
            "snippet": "Experienced Python developer at Google.",
            "link": "https://linkedin.com/in/johndoe"
        }
    ]
}

MOCK_EMPTY_RESPONSE = {
    "organic_results": []
}

MOCK_FAILURE_RESPONSE = {
    "error": "Invalid API Key"
}

@pytest.fixture
def serp_api_key():
    return "fake-serp-api-key"

# Test case for successful lead retrieval
@patch("requests.get")
def test_find_leads_success(mock_get, serp_api_key):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = MOCK_SUCCESS_RESPONSE

    leads = find_leads("developer", "New York", serp_api_key)

    assert isinstance(leads, list)
    assert len(leads) == 1
    assert leads[0]["name"] == "John Doe"
    assert leads[0]["profile_link"] == "https://linkedin.com/in/johndoe"
    assert leads[0]["details"] == "Experienced Python developer at Google."

# Test case for empty results
@patch("requests.get")
def test_find_leads_empty_result(mock_get, serp_api_key):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = MOCK_EMPTY_RESPONSE

    leads = find_leads("unknown-role", "Nowhere", serp_api_key)

    assert isinstance(leads, list)
    assert len(leads) == 0  # Should return an empty list

# Test case for API failure
@patch("requests.get")
def test_find_leads_api_failure(mock_get, serp_api_key):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = MOCK_FAILURE_RESPONSE

    result = find_leads("developer", "New York", serp_api_key)

    assert isinstance(result, dict)
    assert "error" in result
    assert result["error"] == "Failed to fetch data from SerpAPI"
