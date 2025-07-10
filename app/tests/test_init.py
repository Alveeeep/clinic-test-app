from datetime import datetime

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_nonexistent_appointment(client):
    response = await client.get("/appointments/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Appointment not found"}


@pytest.mark.asyncio
async def test_create_appointment(client):
    appointment_data = {
        "patient_name": "Иванов Иван",
        "doctor_id": 1,
        "start_time": datetime(2025, 7, 10, 4, 30).isoformat(),
    }

    create_response = await client.post("/appointments", json=appointment_data)
    assert create_response.status_code == status.HTTP_200_OK
    assert create_response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_invalid_appointment(client):
    invalid_data = {
        "patient_name": "",
        "doctor_id": 1,
        "start_time": datetime(2025, 7, 10, 14, 30).isoformat(),
    }

    response = await client.post("/appointments", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_duplicate_appointment(client):
    appointment_data = {
        "patient_name": "Петров Петр",
        "doctor_id": 2,
        "start_time": datetime(2025, 7, 11, 10, 0).isoformat(),
    }

    response1 = await client.post("/appointments", json=appointment_data)
    assert response1.status_code == status.HTTP_200_OK

    response2 = await client.post("/appointments", json=appointment_data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
