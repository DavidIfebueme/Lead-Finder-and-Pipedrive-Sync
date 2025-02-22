# import pytest
# import requests
# from app.pipedrive import push_to_pipedrive

# @pytest.fixture
# def sample_leads():
#     return [{"name": "John Doe", "profile_link": "https://linkedin.com/johndoe", "details": "Senior Developer"}]

# def test_push_to_pipedrive_success(sample_leads, monkeypatch):
#     class MockResponse:
#         status_code = 201
#         def json(self):
#             return {"data": {"id": 123}}

#     def mock_post(*args, **kwargs):
#         return MockResponse()

#     monkeypatch.setattr(requests, "post", mock_post)
#     response = push_to_pipedrive(sample_leads)
    
#     assert isinstance(response, list)
#     assert response[0]["lead"]["id"] == 123

# def test_push_to_pipedrive_failure(sample_leads, monkeypatch):
#     class MockResponse:
#         status_code = 400
#         def json(self):
#             return {"error": "Invalid request"}

#     def mock_post(*args, **kwargs):
#         return MockResponse()

#     monkeypatch.setattr(requests, "post", mock_post)
#     response = push_to_pipedrive(sample_leads)
    
#     assert isinstance(response, list)
#     assert response[0]["error"] is True
