"""Funciones de apoyo para las pruebas de integración del API."""

from fastapi.testclient import TestClient

CLAVES_PROYECTO = {"id", "nombre"}
CLAVES_ACTIVIDAD = {
    "id",
    "proyecto_id",
    "nombre",
    "presupuesto_total",
    "porcentaje_planificado",
    "porcentaje_real",
    "costo_real",
    "indicadores",
}
CLAVES_INDICADORES = {
    "valor_planificado",
    "valor_ganado",
    "variacion_costo",
    "variacion_cronograma",
    "cpi",
    "spi",
    "eac",
    "vac",
    "interpretacion_costo",
    "interpretacion_cronograma",
}


def datos_actividad(**cambios) -> dict:
    """Actividad de ejemplo: BAC 1000, planificado 50%, real 40%, AC 600."""
    datos = {
        "nombre": "Desarrollar el bot",
        "presupuesto_total": 1000,
        "porcentaje_planificado": 50,
        "porcentaje_real": 40,
        "costo_real": 600,
    }
    datos.update(cambios)
    return datos


def crear_proyecto(cliente: TestClient, nombre: str = "Proyecto de prueba") -> dict:
    respuesta = cliente.post("/proyectos", json={"nombre": nombre})
    assert respuesta.status_code == 201
    return respuesta.json()


def crear_actividad(cliente: TestClient, proyecto_id: int, **cambios) -> dict:
    respuesta = cliente.post(
        f"/proyectos/{proyecto_id}/actividades", json=datos_actividad(**cambios)
    )
    assert respuesta.status_code == 201
    return respuesta.json()
