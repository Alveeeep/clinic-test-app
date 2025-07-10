from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import AppointmentsDAO
from app.dependencies.dao_dep import (
    get_session_with_commit,
    get_session_without_commit,
)
from app.schemas.appointment import AppointmentCreate, AppointmentDTO


router = APIRouter(tags=["Appointments"])


@router.get("/appointments/{id}")
async def get_appointment_by_id(
    id: int, session: AsyncSession = Depends(get_session_without_commit)
) -> dict:
    res = await AppointmentsDAO(session=session).find_one_or_none_by_id(data_id=id)
    if not res:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {
        "status": "ok",
        "result": [AppointmentDTO.model_validate(el) for el in res],
    }


@router.post("/appointments")
async def create_appointment(
    appointment: AppointmentCreate,
    session: AsyncSession = Depends(get_session_with_commit),
) -> dict:
    await AppointmentsDAO(session=session).add(appointment)
    return {"status": "ok"}
