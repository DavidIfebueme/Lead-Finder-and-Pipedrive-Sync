from unittest.mock import patch
import pytest
from app.pipedrive import create_person, push_to_pipedrive

@patch("app.pipedrive.requests.post")
def test_create_person_success(mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"data": {"id": 123}}

    person_id = create_person("John Doe", "test_api_key")
    assert person_id == 123

@patch("app.pipedrive.requests.post")
def test_create_person_failure(mock_post):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"error": "Invalid request"}

    person_id = create_person("John Doe", "test_api_key")
    assert person_id is None

@patch("app.pipedrive.create_person", return_value=456)
@patch("app.pipedrive.requests.post")
def test_push_to_pipedrive_success(mock_post, mock_create_person):
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data

        def json(self):
            return self._json_data

    mock_post.side_effect = [
        MockResponse(201, {"data": {"id": 789}}),  # Successful lead creation
        MockResponse(201, {})  # Successful note creation
    ]

    leads = [{"name": "Jane Doe", "profile_link": "https://linkedin.com/janedoe", "details": "Experienced sales rep"}]
    responses = push_to_pipedrive(leads, "test_api_key")

    assert responses[0]["lead"]["id"] == 789
    assert responses[0]["note_status"] == 201

@patch("app.pipedrive.create_person", return_value=456)
@patch("app.pipedrive.requests.post")
def test_push_to_pipedrive_fail_lead_creation(mock_post, mock_create_person):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"error": "Bad request"}

    leads = [{"name": "Jane Doe", "profile_link": "https://linkedin.com/janedoe", "details": "Experienced sales rep"}]
    responses = push_to_pipedrive(leads, "test_api_key")

    assert responses[0]["error"] is True
    assert responses[0]["status_code"] == 400

@patch("app.pipedrive.create_person", return_value=456)
@patch("app.pipedrive.requests.post")
def test_push_to_pipedrive_missing_lead_id(mock_post, mock_create_person):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"data": {}}

    leads = [{"name": "Jane Doe", "profile_link": "https://linkedin.com/janedoe", "details": "Experienced sales rep"}]
    responses = push_to_pipedrive(leads, "test_api_key")

    assert responses[0]["error"] is True
    assert responses[0]["message"] == "Lead ID not found in response."

