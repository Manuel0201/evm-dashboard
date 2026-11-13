"""Punto de entrada del API. Arranque: uvicorn app.main:app --reload"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.routers import actividades, proyectos
from app.servicios.errores import RecursoNoEncontradoError


def responder_recurso_no_encontrado(
    solicitud: Request, error: RecursoNoEncontradoError
) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(error)})


def crear_aplicacion() -> FastAPI:
    aplicacion = FastAPI(title="EVM Dashboard API", version="1.0.0")
    aplicacion.include_router(proyectos.router)
    aplicacion.include_router(actividades.router)
    aplicacion.add_exception_handler(RecursoNoEncontradoError, responder_recurso_no_encontrado)
    return aplicacion


app = crear_aplicacion()
