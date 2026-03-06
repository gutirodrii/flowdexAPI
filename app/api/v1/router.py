from fastapi import APIRouter
from app.api.v1.endpoints import auth, usuarios, mercados, equipos, clientes, proyectos, tareas, timesheets, logs

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(mercados.router, prefix="/mercados", tags=["mercados"])
api_router.include_router(equipos.router, prefix="/equipos", tags=["equipos"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
api_router.include_router(proyectos.router, prefix="/proyectos", tags=["proyectos"])
api_router.include_router(tareas.router, prefix="", tags=["tareas"])
api_router.include_router(timesheets.router, prefix="/timesheets", tags=["timesheets"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
