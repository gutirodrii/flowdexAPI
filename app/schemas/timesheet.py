import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClockInRequest(BaseModel):
    proyecto_id: Optional[uuid.UUID] = None
    tarea_id: Optional[uuid.UUID] = None
    notas: Optional[str] = None


class ClockOutRequest(BaseModel):
    notas: Optional[str] = None


class TimesheetResponse(BaseModel):
    timesheet_id: uuid.UUID
    usuario_id: uuid.UUID
    proyecto_id: Optional[uuid.UUID] = None
    tarea_id: Optional[uuid.UUID] = None
    status: str
    clock_in: datetime
    clock_out: Optional[datetime] = None
    minutes_worked: int
    notas: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
