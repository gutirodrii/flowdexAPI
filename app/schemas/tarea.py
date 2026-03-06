import uuid
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: str = "todo"
    prioridad: str = "medium"
    asignado_a: Optional[uuid.UUID] = None
    fecha_vencimiento: Optional[date] = None


class TareaCreate(TareaBase):
    pass


class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    prioridad: Optional[str] = None
    asignado_a: Optional[uuid.UUID] = None
    fecha_vencimiento: Optional[date] = None


class TareaResponse(TareaBase):
    tarea_id: uuid.UUID
    proyecto_id: uuid.UUID
    creada_por: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
