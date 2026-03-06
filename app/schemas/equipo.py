import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EquipoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class EquipoCreate(EquipoBase):
    pass


class EquipoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class EquipoResponse(EquipoBase):
    equipo_id: uuid.UUID
    created_by: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class MiembroAdd(BaseModel):
    usuario_id: uuid.UUID
    rol_equipo: str = "member"


class MiembroResponse(BaseModel):
    equipo_id: uuid.UUID
    usuario_id: uuid.UUID
    rol_equipo: str
    joined_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
