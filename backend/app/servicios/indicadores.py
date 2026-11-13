"""Indicadores consolidados de un proyecto."""

from sqlalchemy.orm import Session

from app.calculos.evm import calcular_indicadores_proyecto
from app.calculos.tipos import Indicadores
from app.servicios.actividades import convertir_a_datos_de_calculo
from app.servicios.proyectos import obtener_proyecto


def calcular_indicadores_del_proyecto(sesion: Session, proyecto_id: int) -> Indicadores:
    """Suma los montos de todas las actividades del proyecto y recalcula los índices."""
    proyecto = obtener_proyecto(sesion, proyecto_id)
    datos = [convertir_a_datos_de_calculo(actividad) for actividad in proyecto.actividades]
    return calcular_indicadores_proyecto(datos)
