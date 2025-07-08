from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.appointment import AppointmentDTO, AppointmentCreate
from app.dao.dao import AppointmentsDAO
from app.dependencies.dao_dep import get_session_with_commit

router = APIRouter(tags=['Appointments'])

@router.get("/appointments/{id}")
async def get_appointment_by_id(id: int, session: AsyncSession = Depends(get_session_with_commit)) -> dict:
    try:
        res = await AppointmentsDAO(session=session).find_one_or_none_by_id(data_id=id)
        return {'status': 'ok', 'result': [AppointmentDTO.model_validate(el) for el in res]}
    except Exception as e:
        return {'status': 'error', "error": e}

@router.post("/appointments")
async def create_appointment(appointment: AppointmentCreate, session: AsyncSession = Depends(get_session_with_commit)) -> dict:
    try:
        await AppointmentsDAO(session=session).add(appointment)
        return {'status': 'ok'}
    except Exception as e:
        return {'status': 'error', "error": e}

