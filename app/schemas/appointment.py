from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AppointmentCreate(BaseModel):
    patient_name: str
    doctor_id: int
    start_time: datetime


class AppointmentDTO(AppointmentCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
