from app.dao.base import BaseDAO
from app.models.appointments import Appointment

class AppointmentsDAO(BaseDAO[Appointment]):
    model = Appointment
