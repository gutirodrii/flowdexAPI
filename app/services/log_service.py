import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.log import Log


async def write_log(
    db: AsyncSession,
    entity: str,
    entity_id: Optional[uuid.UUID],
    action: str,
    usuario_id: Optional[uuid.UUID],
    old_data: Optional[dict] = None,
    new_data: Optional[dict] = None,
    level: str = "info",
    message: Optional[str] = None,
) -> None:
    log = Log(
        entity=entity,
        entity_id=entity_id,
        action=action,
        usuario_id=usuario_id,
        old_data=old_data,
        new_data=new_data,
        level=level,
        message=message,
    )
    db.add(log)
    await db.flush()
