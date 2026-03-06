import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MercadoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class MercadoCreate(MercadoBase):
    pass


class MercadoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class MercadoResponse(MercadoBase):
    mercado_id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
