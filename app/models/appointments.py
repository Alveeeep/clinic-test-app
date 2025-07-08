from datetime import datetime
from app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from datetime import date
from sqlalchemy import ForeignKey


class Appointment(Base):
    patient_name: Mapped[str]
    doctor_id: Mapped[int]
    start_time: Mapped[datetime]
    UniqueConstraint('doctor_id', 'start_time', name="unique_doc_time")
