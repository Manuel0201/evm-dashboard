"""Operaciones sobre actividades. Cada actividad sale con sus indicadores EVM."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.calculos.evm import calcular_indicadores_actividad
from app.calculos.tipos import DatosActividad
from app.esquemas import ActividadEntrada, ActividadSalida, IndicadoresSalida
from app.modelos import Actividad
from app.servicios.errores import RecursoNoEncontradoError
from app.servicios.proyectos import obtener_proyecto

NOMBRE_RECURSO_ACTIVIDAD = "Actividad"


def convertir_a_datos_de_calculo(actividad: Actividad) -> DatosActividad:
    """Traduce una fila de la base de datos a lo que esperan las fórmulas EVM."""
    return DatosActividad(
        presupuesto_total=actividad.presupuesto_total,
        porcentaje_planificado=actividad.porcentaje_planificado,
        porcentaje_real=actividad.porcentaje_real,
        costo_real=actividad.costo_real,
    )


def construir_actividad_salida(actividad: Actividad) -> ActividadSalida:
    indicadores = calcular_indicadores_actividad(convertir_a_datos_de_calculo(actividad))
    return ActividadSalida(
        id=actividad.id,
        proyecto_id=actividad.proyecto_id,
        nombre=actividad.nombre,
        presupuesto_total=actividad.presupuesto_total,
        porcentaje_planificado=actividad.porcentaje_planificado,
        porcentaje_real=actividad.porcentaje_real,
        costo_real=actividad.costo_real,
        indicadores=IndicadoresSalida.model_validate(indicadores),
    )


def obtener_actividad(sesion: Session, actividad_id: int) -> Actividad:
    actividad = sesion.get(Actividad, actividad_id)
    if actividad is None:
        raise RecursoNoEncontradoError(NOMBRE_RECURSO_ACTIVIDAD, actividad_id)
    return actividad


def crear_actividad(sesion: Session, proyecto_id: int, datos: ActividadEntrada) -> ActividadSalida:
    proyecto = obtener_proyecto(sesion, proyecto_id)
    actividad = Actividad(proyecto_id=proyecto.id, **datos.model_dump())
    sesion.add(actividad)
    sesion.commit()
    return construir_actividad_salida(actividad)


def listar_actividades(sesion: Session, proyecto_id: int) -> list[ActividadSalida]:
    proyecto = obtener_proyecto(sesion, proyecto_id)
    consulta = select(Actividad).where(Actividad.proyecto_id == proyecto.id).order_by(Actividad.id)
    return [construir_actividad_salida(actividad) for actividad in sesion.scalars(consulta)]


def actualizar_actividad(
    sesion: Session, actividad_id: int, datos: ActividadEntrada
) -> ActividadSalida:
    actividad = obtener_actividad(sesion, actividad_id)
    for campo, valor in datos.model_dump().items():
        setattr(actividad, campo, valor)
    sesion.commit()
    return construir_actividad_salida(actividad)


def eliminar_actividad(sesion: Session, actividad_id: int) -> None:
    sesion.delete(obtener_actividad(sesion, actividad_id))
    sesion.commit()
