# import pytest
# from app import app

# @pytest.fixture
# def client():
#     app.testing = True
#     return app.test_client()

# def test_process_message_success(client, monkeypatch):
#     def mock_find_leads(role, location, api_key):
#         return [{"name": "Jane Doe", "profile_link": "https://linkedin.com/janedoe", "details": "Designer"}]

#     def mock_push_to_pipedrive(leads):
#         return [{"lead": {"id": 123}}]

#     monkeypatch.setattr("app.lead_finder.find_leads", mock_find_leads)
#     monkeypatch.setattr("app.pipedrive.push_to_pipedrive", mock_push_to_pipedrive)

#     response = client.post("/process-message", json={
#         "message": "find designer in New York",
#         "pipedrive_api_key": "fake-key",
#         "serp_api_key": "fake-key"
#     })

#     assert response.status_code == 200
#     assert b"Found and pushed 1 leads to Pipedrive" in response.data

# def test_process_message_invalid_request(client):
#     response = client.post("/process-message", json={})
#     assert response.status_code == 400
