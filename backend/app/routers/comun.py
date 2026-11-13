"""Piezas que comparten los routers."""

from typing import Annotated

from fastapi import Depends, status
from sqlalchemy.orm import Session

from app.base_de_datos import obtener_sesion
from app.esquemas import ErrorSalida

SesionDeBaseDeDatos = Annotated[Session, Depends(obtener_sesion)]

RESPUESTA_NO_ENCONTRADO = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorSalida,
        "description": "El proyecto o la actividad no existe",
    }
}
