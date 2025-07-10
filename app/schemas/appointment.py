from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    patient_name: str = Field(min_length=3)
    doctor_id: int = Field(gt=0)
    start_time: datetime


class AppointmentDTO(AppointmentCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
