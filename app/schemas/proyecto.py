import uuid
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class ProyectoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    mercado_id: Optional[uuid.UUID] = None
    cliente_id: Optional[uuid.UUID] = None
    equipo_id: Optional[uuid.UUID] = None
    owner_usuario_id: Optional[uuid.UUID] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    mercado_id: Optional[uuid.UUID] = None
    cliente_id: Optional[uuid.UUID] = None
    equipo_id: Optional[uuid.UUID] = None
    owner_usuario_id: Optional[uuid.UUID] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class ProyectoResponse(ProyectoBase):
    proyecto_id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
