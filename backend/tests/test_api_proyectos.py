"""Pruebas de integración de los endpoints de proyectos."""

import pytest
from fastapi.testclient import TestClient

from tests.ayudas import CLAVES_PROYECTO, crear_actividad, crear_proyecto

PROYECTO_INEXISTENTE = 999999
MENSAJE_PROYECTO_INEXISTENTE = "Proyecto 999999 no existe"


def test_crear_proyecto_devuelve_201_y_el_contrato_esperado(cliente: TestClient):
    respuesta = cliente.post("/proyectos", json={"nombre": "Migración de facturación"})

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert set(cuerpo) == CLAVES_PROYECTO
    assert isinstance(cuerpo["id"], int)
    assert cuerpo["nombre"] == "Migración de facturación"


@pytest.mark.parametrize("nombre", ["", "   "])
def test_crear_proyecto_rechaza_nombre_vacio(cliente: TestClient, nombre: str):
    respuesta = cliente.post("/proyectos", json={"nombre": nombre})

    assert respuesta.status_code == 422


def test_crear_proyecto_rechaza_cuerpo_sin_nombre(cliente: TestClient):
    respuesta = cliente.post("/proyectos", json={})

    assert respuesta.status_code == 422


def test_listar_proyectos_devuelve_lista_vacia_si_no_hay_ninguno(cliente: TestClient):
    respuesta = cliente.get("/proyectos")

    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_listar_proyectos_devuelve_todos_en_orden_de_creacion(cliente: TestClient):
    crear_proyecto(cliente, "Primero")
    crear_proyecto(cliente, "Segundo")

    respuesta = cliente.get("/proyectos")

    assert respuesta.status_code == 200
    assert [proyecto["nombre"] for proyecto in respuesta.json()] == ["Primero", "Segundo"]
    assert all(set(proyecto) == CLAVES_PROYECTO for proyecto in respuesta.json())


def test_consultar_proyecto_devuelve_el_proyecto(cliente: TestClient):
    proyecto = crear_proyecto(cliente, "Consultable")

    respuesta = cliente.get(f"/proyectos/{proyecto['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"id": proyecto["id"], "nombre": "Consultable"}


def test_consultar_proyecto_inexistente_devuelve_404(cliente: TestClient):
    respuesta = cliente.get(f"/proyectos/{PROYECTO_INEXISTENTE}")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": MENSAJE_PROYECTO_INEXISTENTE}


def test_editar_proyecto_cambia_el_nombre(cliente: TestClient):
    proyecto = crear_proyecto(cliente, "Nombre viejo")

    respuesta = cliente.put(f"/proyectos/{proyecto['id']}", json={"nombre": "Nombre nuevo"})

    assert respuesta.status_code == 200
    assert respuesta.json() == {"id": proyecto["id"], "nombre": "Nombre nuevo"}
    assert cliente.get(f"/proyectos/{proyecto['id']}").json()["nombre"] == "Nombre nuevo"


def test_editar_proyecto_inexistente_devuelve_404(cliente: TestClient):
    respuesta = cliente.put(f"/proyectos/{PROYECTO_INEXISTENTE}", json={"nombre": "X"})

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": MENSAJE_PROYECTO_INEXISTENTE}


def test_editar_proyecto_rechaza_nombre_vacio(cliente: TestClient):
    proyecto = crear_proyecto(cliente)

    respuesta = cliente.put(f"/proyectos/{proyecto['id']}", json={"nombre": ""})

    assert respuesta.status_code == 422


def test_eliminar_proyecto_devuelve_204_y_ya_no_existe(cliente: TestClient):
    proyecto = crear_proyecto(cliente)

    respuesta = cliente.delete(f"/proyectos/{proyecto['id']}")

    assert respuesta.status_code == 204
    assert respuesta.content == b""
    assert cliente.get(f"/proyectos/{proyecto['id']}").status_code == 404


def test_eliminar_proyecto_elimina_sus_actividades(cliente: TestClient):
    proyecto = crear_proyecto(cliente)
    actividad = crear_actividad(cliente, proyecto["id"])

    cliente.delete(f"/proyectos/{proyecto['id']}")

    assert cliente.delete(f"/actividades/{actividad['id']}").status_code == 404


def test_eliminar_proyecto_inexistente_devuelve_404(cliente: TestClient):
    respuesta = cliente.delete(f"/proyectos/{PROYECTO_INEXISTENTE}")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": MENSAJE_PROYECTO_INEXISTENTE}
