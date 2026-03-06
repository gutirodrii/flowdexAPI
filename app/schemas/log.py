import uuid
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel


class LogResponse(BaseModel):
    log_id: int
    created_at: Optional[datetime] = None
    usuario_id: Optional[uuid.UUID] = None
    entity: str
    entity_id: Optional[uuid.UUID] = None
    action: str
    level: str
    message: Optional[str] = None
    old_data: Optional[Any] = None
    new_data: Optional[Any] = None

    model_config = {"from_attributes": True}
