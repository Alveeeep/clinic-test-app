from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped

from app.database.db import Base


class Appointment(Base):
    patient_name: Mapped[str]
    doctor_id: Mapped[int]
    start_time: Mapped[datetime]
    UniqueConstraint("doctor_id", "start_time", name="unique_doc_time")
