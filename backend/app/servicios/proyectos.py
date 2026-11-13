"""Operaciones sobre proyectos."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.esquemas import ProyectoEntrada
from app.modelos import Proyecto
from app.servicios.errores import RecursoNoEncontradoError

NOMBRE_RECURSO_PROYECTO = "Proyecto"


def obtener_proyecto(sesion: Session, proyecto_id: int) -> Proyecto:
    proyecto = sesion.get(Proyecto, proyecto_id)
    if proyecto is None:
        raise RecursoNoEncontradoError(NOMBRE_RECURSO_PROYECTO, proyecto_id)
    return proyecto


def crear_proyecto(sesion: Session, datos: ProyectoEntrada) -> Proyecto:
    proyecto = Proyecto(nombre=datos.nombre)
    sesion.add(proyecto)
    sesion.commit()
    return proyecto


def listar_proyectos(sesion: Session) -> list[Proyecto]:
    return list(sesion.scalars(select(Proyecto).order_by(Proyecto.id)))


def actualizar_proyecto(sesion: Session, proyecto_id: int, datos: ProyectoEntrada) -> Proyecto:
    proyecto = obtener_proyecto(sesion, proyecto_id)
    proyecto.nombre = datos.nombre
    sesion.commit()
    return proyecto


def eliminar_proyecto(sesion: Session, proyecto_id: int) -> None:
    sesion.delete(obtener_proyecto(sesion, proyecto_id))
    sesion.commit()
