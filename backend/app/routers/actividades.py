"""Endpoints de actividades. Cada actividad se devuelve con sus indicadores EVM."""

from fastapi import APIRouter, status

from app.esquemas import ActividadEntrada, ActividadSalida
from app.routers.comun import RESPUESTA_NO_ENCONTRADO, SesionDeBaseDeDatos
from app.servicios import actividades as servicio_actividades

router = APIRouter(tags=["Actividades"])


@router.post(
    "/proyectos/{proyecto_id}/actividades",
    response_model=ActividadSalida,
    status_code=status.HTTP_201_CREATED,
    responses=RESPUESTA_NO_ENCONTRADO,
    summary="Crear una actividad",
    description="Crea una actividad dentro de un proyecto y devuelve sus indicadores EVM.",
)
def crear_actividad(proyecto_id: int, datos: ActividadEntrada, sesion: SesionDeBaseDeDatos):
    return servicio_actividades.crear_actividad(sesion, proyecto_id, datos)


@router.get(
    "/proyectos/{proyecto_id}/actividades",
    response_model=list[ActividadSalida],
    responses=RESPUESTA_NO_ENCONTRADO,
    summary="Listar las actividades de un proyecto",
    description="Devuelve las actividades del proyecto, cada una con sus indicadores EVM.",
)
def listar_actividades(proyecto_id: int, sesion: SesionDeBaseDeDatos):
    return servicio_actividades.listar_actividades(sesion, proyecto_id)


@router.put(
    "/actividades/{actividad_id}",
    response_model=ActividadSalida,
    responses=RESPUESTA_NO_ENCONTRADO,
    summary="Editar una actividad",
    description="Reemplaza los datos de una actividad y devuelve sus indicadores recalculados.",
)
def editar_actividad(actividad_id: int, datos: ActividadEntrada, sesion: SesionDeBaseDeDatos):
    return servicio_actividades.actualizar_actividad(sesion, actividad_id, datos)


@router.delete(
    "/actividades/{actividad_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=RESPUESTA_NO_ENCONTRADO,
    summary="Eliminar una actividad",
    description="Elimina una actividad.",
)
def eliminar_actividad(actividad_id: int, sesion: SesionDeBaseDeDatos) -> None:
    servicio_actividades.eliminar_actividad(sesion, actividad_id)
