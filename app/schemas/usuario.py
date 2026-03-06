import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    email: str
    rol: str = "user"
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None
    password: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    usuario_id: uuid.UUID
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
