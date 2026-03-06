from app.models.mercado import Mercado
from app.schemas.mercado import MercadoCreate, MercadoUpdate
from app.repositories.base import BaseRepository


class MercadoRepository(BaseRepository[Mercado, MercadoCreate, MercadoUpdate]):
    def __init__(self):
        super().__init__(Mercado, "mercado_id")


mercado_repository = MercadoRepository()
