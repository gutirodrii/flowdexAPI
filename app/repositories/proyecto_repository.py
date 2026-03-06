from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate
from app.repositories.base import BaseRepository


class ProyectoRepository(BaseRepository[Proyecto, ProyectoCreate, ProyectoUpdate]):
    def __init__(self):
        super().__init__(Proyecto, "proyecto_id")


proyecto_repository = ProyectoRepository()
