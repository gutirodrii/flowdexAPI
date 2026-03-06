import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClienteBase(BaseModel):
    nif: str
    nombre_comercial: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    cp: Optional[str] = None
    pais: str = "ES"
    activo: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre_comercial: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    cp: Optional[str] = None
    pais: Optional[str] = None
    activo: Optional[bool] = None


class ClienteResponse(ClienteBase):
    cliente_id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
