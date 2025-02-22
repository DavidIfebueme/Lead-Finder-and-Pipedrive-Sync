# import pytest
# from app.lead_finder import find_leads

# def test_find_leads_success():
#     leads = find_leads("developer", "New York", "fake-serp-api-key")
#     assert isinstance(leads, list)
#     assert all(isinstance(lead, dict) for lead in leads)

# def test_find_leads_empty_result():
#     leads = find_leads("unknown-role", "Nowhere", "fake-serp-api-key")
#     assert isinstance(leads, list)
#     assert len(leads) == 0
