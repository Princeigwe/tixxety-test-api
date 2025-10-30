from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

client = TestClient(app)

mock_bearer_token = "Bearer eyJ.mock-token"

mock_event_database = [
  {
    "start_date": "2025-10-29",
    "title": "Scholars Club",
    "city": "Aba",
    "country": "Nigeria",
    "tickets_sold": 0,
    "description": "Event to mingle with fellow scholars",
    "id": "89efa541-3860-46a8-a8b8-f9fd6760c3a0",
    "end_date": "2025-11-23",
    "street": "209, HEavenly Street",
    "state": "Abia",
    "total_tickets": 2,
    "created_at": "2025-10-29T22:09:36.008451"
  },
  {
    "start_date": "2025-10-29",
    "title": "Foodies in the House",
    "city": "Lagos",
    "country": "Nigeria",
    "tickets_sold": 1,
    "description": "Foodie event. Eat away.",
    "id": "4b45e744-1416-41ff-ae4b-f7345f57a8c4",
    "end_date": "2025-11-23",
    "street": "209, Fake Street",
    "state": "Lagos",
    "total_tickets": 5,
    "created_at": "2025-10-29T22:07:40.261874"
  }
]


mock_ticket_database = [
  {
    "event_id": "4b45e744-1416-41ff-ae4b-f7345f57a8c4",
    "status": "reserved",
    "created_at": "2025-10-29T22:17:39.524362",
    "id": "c5c8741a-a58c-4b4d-9e3e-7562731e7ab4",
    "user_id": "409f9108-891f-42a1-99e9-d3e9e33ce615"
  }
]


mock_api_ticket_response ={
    "event_id": "89efa541-3860-46a8-a8b8-f9fd6760c3a0",
    "status": "reserved",
    "created_at": "2025-10-29T22:18:10.345678",
    "id": "d2f5e1c3-4b6e-4c2a-9f7e-123456789abc",
    "user_id": "409f9108-891f-42a1-99e9-d3e9e33ce615"
  }


def test_reserve_ticket_event_not_found():
  response = client.post(
    "/tickets/",
    headers={"Authorization": mock_bearer_token},
    json={"event_id": "non-existing-event-id"}
  )
  assert response.status_code == 404


def test_reserve_ticket_already_reserved():
  response = client.post(
    "/tickets/",
    headers={"Authorization": mock_bearer_token},
    json={"event_id": "4b45e744-1416-41ff-ae4b-f7345f57a8c4"}
  )
  event_id = "4b45e744-1416-41ff-ae4b-f7345f57a8c4"
  user_id_to_check = "4409f9108-891f-42a1-99e9-d3e9e33ce615"

  # checking if the user has already reserved a ticket for the event
  for ticket in mock_ticket_database:
    if ticket["event_id"] == event_id and ticket["user_id"] == user_id_to_check:
      assert response.status_code == 400


def test_reserve_ticket_success():
  response = client.post(
    "/tickets/",
    headers={"Authorization": mock_bearer_token},
    json={"event_id": "89efa541-3860-46a8-a8b8-f9fd6760c3a0"}
  )
  event_id = "89efa541-3860-46a8-a8b8-f9fd6760c3a0"
  user_id_to_check = "4409f9108-891f-42a1-99e9-d3e9e33ce615"

  # checking if the user has already reserved a ticket for the event
  for ticket in mock_ticket_database:
    if ticket["event_id"] == event_id and ticket["user_id"] == user_id_to_check:
      assert response.status_code == 200
  

