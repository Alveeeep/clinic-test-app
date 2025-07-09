import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.dao.dao import AppointmentsDAO
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.schemas.appointment import AppointmentCreate


def test_create_appointment(session: AsyncSession = Depends(get_session_with_commit)):
    dao = AppointmentsDAO(session=session)
    data = {
        'patient_name': 'ТестЮзер123',
        'doctor_id': 1,
        'start_time': datetime.now()
    }
    appointment = AppointmentCreate(**data)
    assert dao.add(appointment)


def test_create_bad_pair(session: AsyncSession = Depends(get_session_with_commit)):
    dao = AppointmentsDAO(session=session)
    data1 = {
        'patient_name': 'ТестЮзер222',
        'doctor_id': 2,
        'start_time': datetime(2025, 7, 9, 22, 30, 10)
    }
    data2 = {
        'patient_name': 'ТестЮзер333',
        'doctor_id': 2,
        'start_time': datetime(2025, 7, 9, 22, 30, 10)
    }
    assert dao.add(AppointmentCreate(**data1))
    assert dao.add(AppointmentCreate(**data2))
