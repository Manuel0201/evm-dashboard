"""Punto de entrada del API. Arranque: uvicorn app.main:app --reload"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.routers import actividades, proyectos
from app.servicios.errores import RecursoNoEncontradoError

RUTA_DOCUMENTACION = "/api-docs"
VERSION_API = "1.0.1"
DESCRIPCION_API = """
API REST para gestionar proyectos y actividades y calcular automáticamente los indicadores
de **Valor Ganado (EVM)**.

**Datos de cada actividad:** nombre, BAC (presupuesto total), % de avance planificado,
% de avance real y AC (costo real). Los porcentajes van de 0 a 100.

**Indicadores calculados al vuelo** (por actividad y consolidados por proyecto):
PV = % planificado x BAC, EV = % real x BAC, CV = EV - AC, SV = EV - PV,
CPI = EV / AC, SPI = EV / PV, EAC = BAC / CPI y VAC = BAC - EAC.

**Consolidado del proyecto:** se suman BAC, PV, EV y AC de las actividades y los índices
se recalculan sobre esos totales.

**Indicador `null`:** significa que no se puede calcular por una división por cero
(por ejemplo, CPI con AC = 0). La interpretación correspondiente es "No calculable".

**Errores:** `404` si el proyecto o la actividad no existe; `422` si los datos enviados
no son válidos.
"""
ETIQUETAS = [
    {"name": "Proyectos", "description": "Crear, consultar, editar y eliminar proyectos."},
    {
        "name": "Actividades",
        "description": "Actividades de un proyecto; cada una trae sus indicadores EVM.",
    },
]


def responder_recurso_no_encontrado(
    solicitud: Request, error: RecursoNoEncontradoError
) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(error)})


def crear_aplicacion() -> FastAPI:
    aplicacion = FastAPI(
        title="EVM Dashboard API",
        version=VERSION_API,
        description=DESCRIPCION_API,
        openapi_tags=ETIQUETAS,
        docs_url=RUTA_DOCUMENTACION,
        redoc_url=None,
    )
    aplicacion.include_router(proyectos.router)
    aplicacion.include_router(actividades.router)
    aplicacion.add_exception_handler(RecursoNoEncontradoError, responder_recurso_no_encontrado)
    return aplicacion


app = crear_aplicacion()
