"""Endpoints de proyectos y de sus indicadores consolidados."""

from fastapi import APIRouter, status

from app.esquemas import IndicadoresSalida, ProyectoEntrada, ProyectoSalida
from app.routers.comun import RESPUESTA_NO_ENCONTRADO, SesionDeBaseDeDatos
from app.servicios import indicadores as servicio_indicadores
from app.servicios import proyectos as servicio_proyectos

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.post(
    "",
    response_model=ProyectoSalida,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un proyecto",
    description="Crea un proyecto vacío. Las actividades se agregan después.",
)
def crear_proyecto(datos: ProyectoEntrada, sesion: SesionDeBaseDeDatos):
    return servicio_proyectos.crear_proyecto(sesion, datos)


@router.get(
    "",
    response_model=list[ProyectoSalida],
    summary="Listar proyectos",
    description="Devuelve todos los proyectos ordenados por id.",
)
def listar_proyectos(sesion: SesionDeBaseDeDatos):
    return servicio_proyectos.listar_proyectos(sesion)


@router.get(
    "/{proyecto_id}",
    response_model=ProyectoSalida,
    responses=RESPUESTA_NO_ENCONTRADO,
    summary="Consultar un proyecto",
    description="Devuelve un proyecto por su id.",
)
def consultar_proyecto(proyecto_id: int, sesion: SesionDeBaseDeDatos):
    return servicio_proyectos.obtener_proyecto(sesion, proyecto_id)


@router.put(
    "/{proyecto_id}",
    response_model=ProyectoSalida,
    responses=RESPUESTA_NO_ENCONTRADO,
    summary="Editar un proyecto",
    description="Cambia el nombre de un proyecto.",
)
def editar_proyecto(proyecto_id: int, datos: ProyectoEntrada, sesion: SesionDeBaseDeDatos):
    return servicio_proyectos.actualizar_proyecto(sesion, proyecto_id, datos)


@router.delete(
    "/{proyecto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=RESPUESTA_NO_ENCONTRADO,
    summary="Eliminar un proyecto",
    description="Elimina el proyecto y, en cascada, todas sus actividades.",
)
def eliminar_proyecto(proyecto_id: int, sesion: SesionDeBaseDeDatos) -> None:
    servicio_proyectos.eliminar_proyecto(sesion, proyecto_id)


@router.get(
    "/{proyecto_id}/indicadores",
    response_model=IndicadoresSalida,
    responses=RESPUESTA_NO_ENCONTRADO,
    summary="Indicadores consolidados del proyecto",
    description=(
        "Suma BAC, PV, EV y AC de todas las actividades y recalcula CPI, SPI, EAC y VAC "
        "sobre esos totales. Devuelve también la interpretación de CPI y SPI. "
        "Un indicador null significa que no se puede calcular (división por cero)."
    ),
)
def consultar_indicadores_del_proyecto(proyecto_id: int, sesion: SesionDeBaseDeDatos):
    return servicio_indicadores.calcular_indicadores_del_proyecto(sesion, proyecto_id)
