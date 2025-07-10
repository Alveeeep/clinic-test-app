from datetime import datetime

import pytest

from app.dao.dao import AppointmentsDAO
from app.schemas.appointment import AppointmentCreate


@pytest.mark.asyncio
async def test_create_appointment(db_session):
    dao = AppointmentsDAO(session=db_session)
    data = {
        "patient_name": "ТестЮзер123",
        "doctor_id": 1,
        "start_time": datetime.now(),
    }
    appointment = AppointmentCreate(**data)
    result = await dao.add(appointment)
    assert result is not None
    assert result.patient_name == "ТестЮзер123"


@pytest.mark.asyncio
async def test_create_bad_pair(db_session):
    dao = AppointmentsDAO(session=db_session)

    data1 = {
        "patient_name": "ТестЮзер222",
        "doctor_id": 2,
        "start_time": datetime(2025, 7, 9, 22, 30, 10),
    }
    async with db_session.begin():
        first_appointment = await dao.add(AppointmentCreate(**data1))
    assert first_appointment is not None
    data2 = {
        "patient_name": "ТестЮзер333",
        "doctor_id": 2,
        "start_time": datetime(2025, 7, 9, 22, 30, 10),
    }

    with pytest.raises(Exception):
        async with db_session.begin():
            await dao.add(AppointmentCreate(**data2))
