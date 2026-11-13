"""Pruebas de integración de los endpoints de actividades, con valores EVM calculados a mano."""

import pytest
from fastapi.testclient import TestClient

from tests.ayudas import (
    CLAVES_ACTIVIDAD,
    CLAVES_INDICADORES,
    crear_actividad,
    crear_proyecto,
    datos_actividad,
)

PROYECTO_INEXISTENTE = 999999
ACTIVIDAD_INEXISTENTE = 888888
MENSAJE_ACTIVIDAD_INEXISTENTE = "Actividad 888888 no existe"

DATOS_INVALIDOS = [
    pytest.param({"porcentaje_real": 100.01}, id="porcentaje real mayor a 100"),
    pytest.param({"porcentaje_planificado": -1}, id="porcentaje planificado negativo"),
    pytest.param({"porcentaje_real": 40.123}, id="porcentaje con tres decimales"),
    pytest.param({"costo_real": -5}, id="costo real negativo"),
    pytest.param({"presupuesto_total": -1}, id="presupuesto negativo"),
    pytest.param({"nombre": ""}, id="nombre vacio"),
]


def test_crear_actividad_devuelve_201_con_datos_e_indicadores_calculados(cliente: TestClient):
    proyecto = crear_proyecto(cliente)

    respuesta = cliente.post(f"/proyectos/{proyecto['id']}/actividades", json=datos_actividad())

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert set(cuerpo) == CLAVES_ACTIVIDAD
    assert set(cuerpo["indicadores"]) == CLAVES_INDICADORES
    assert cuerpo["proyecto_id"] == proyecto["id"]
    assert cuerpo["nombre"] == "Desarrollar el bot"
    assert cuerpo["presupuesto_total"] == 1000
    assert cuerpo["indicadores"] == {
        "valor_planificado": 500,
        "valor_ganado": 400,
        "variacion_costo": -200,
        "variacion_cronograma": -100,
        "cpi": 0.6667,
        "spi": 0.8,
        "eac": 1500,
        "vac": -500,
        "interpretacion_costo": "Sobre presupuesto",
        "interpretacion_cronograma": "Atrasado",
    }


def test_crear_actividad_con_costo_cero_devuelve_indicadores_nulos(cliente: TestClient):
    proyecto = crear_proyecto(cliente)

    actividad = crear_actividad(cliente, proyecto["id"], costo_real=0)

    indicadores = actividad["indicadores"]
    assert indicadores["cpi"] is None
    assert indicadores["eac"] is None
    assert indicadores["vac"] is None
    assert indicadores["interpretacion_costo"] == "No calculable"
    assert indicadores["spi"] == 0.8


def test_crear_actividad_en_proyecto_inexistente_devuelve_404(cliente: TestClient):
    respuesta = cliente.post(
        f"/proyectos/{PROYECTO_INEXISTENTE}/actividades", json=datos_actividad()
    )

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Proyecto 999999 no existe"}


@pytest.mark.parametrize("cambios", DATOS_INVALIDOS)
def test_crear_actividad_rechaza_datos_invalidos(cliente: TestClient, cambios: dict):
    proyecto = crear_proyecto(cliente)

    respuesta = cliente.post(
        f"/proyectos/{proyecto['id']}/actividades", json=datos_actividad(**cambios)
    )

    assert respuesta.status_code == 422


def test_crear_actividad_rechaza_cuerpo_incompleto(cliente: TestClient):
    proyecto = crear_proyecto(cliente)

    respuesta = cliente.post(
        f"/proyectos/{proyecto['id']}/actividades", json={"nombre": "Solo nombre"}
    )

    assert respuesta.status_code == 422


def test_crear_actividad_acepta_los_limites_cero_y_cien(cliente: TestClient):
    proyecto = crear_proyecto(cliente)

    actividad = crear_actividad(
        cliente, proyecto["id"], porcentaje_planificado=0, porcentaje_real=100
    )

    assert actividad["porcentaje_real"] == 100
    assert actividad["indicadores"]["valor_ganado"] == 1000
    assert actividad["indicadores"]["spi"] is None


def test_listar_actividades_devuelve_cada_una_con_sus_indicadores(cliente: TestClient):
    proyecto = crear_proyecto(cliente)
    crear_actividad(cliente, proyecto["id"], nombre="A")
    crear_actividad(
        cliente,
        proyecto["id"],
        nombre="B",
        presupuesto_total=2000,
        porcentaje_planificado=30,
        porcentaje_real=45,
        costo_real=800,
    )

    respuesta = cliente.get(f"/proyectos/{proyecto['id']}/actividades")

    assert respuesta.status_code == 200
    actividades = respuesta.json()
    assert [actividad["nombre"] for actividad in actividades] == ["A", "B"]
    assert all(set(actividad) == CLAVES_ACTIVIDAD for actividad in actividades)
    assert actividades[0]["indicadores"]["cpi"] == 0.6667
    assert actividades[1]["indicadores"]["cpi"] == 1.125
    assert actividades[1]["indicadores"]["spi"] == 1.5
    assert actividades[1]["indicadores"]["interpretacion_costo"] == "Bajo presupuesto"
    assert actividades[1]["indicadores"]["interpretacion_cronograma"] == "Adelantado"


def test_listar_actividades_solo_incluye_las_del_proyecto_pedido(cliente: TestClient):
    proyecto_uno = crear_proyecto(cliente, "Uno")
    proyecto_dos = crear_proyecto(cliente, "Dos")
    crear_actividad(cliente, proyecto_uno["id"], nombre="Del uno")
    crear_actividad(cliente, proyecto_dos["id"], nombre="Del dos")

    respuesta = cliente.get(f"/proyectos/{proyecto_uno['id']}/actividades")

    assert [actividad["nombre"] for actividad in respuesta.json()] == ["Del uno"]


def test_listar_actividades_de_proyecto_sin_actividades_devuelve_lista_vacia(
    cliente: TestClient,
):
    proyecto = crear_proyecto(cliente)

    respuesta = cliente.get(f"/proyectos/{proyecto['id']}/actividades")

    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_listar_actividades_de_proyecto_inexistente_devuelve_404(cliente: TestClient):
    respuesta = cliente.get(f"/proyectos/{PROYECTO_INEXISTENTE}/actividades")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Proyecto 999999 no existe"}


def test_editar_actividad_recalcula_los_indicadores(cliente: TestClient):
    proyecto = crear_proyecto(cliente)
    actividad = crear_actividad(cliente, proyecto["id"])

    respuesta = cliente.put(
        f"/actividades/{actividad['id']}", json=datos_actividad(porcentaje_real=50)
    )

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert set(cuerpo) == CLAVES_ACTIVIDAD
    assert cuerpo["id"] == actividad["id"]
    assert cuerpo["porcentaje_real"] == 50
    assert cuerpo["indicadores"]["valor_ganado"] == 500
    assert cuerpo["indicadores"]["cpi"] == 0.8333
    assert cuerpo["indicadores"]["spi"] == 1
    assert cuerpo["indicadores"]["interpretacion_cronograma"] == "En tiempo"


def test_editar_actividad_inexistente_devuelve_404(cliente: TestClient):
    respuesta = cliente.put(f"/actividades/{ACTIVIDAD_INEXISTENTE}", json=datos_actividad())

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": MENSAJE_ACTIVIDAD_INEXISTENTE}


@pytest.mark.parametrize("cambios", DATOS_INVALIDOS)
def test_editar_actividad_rechaza_datos_invalidos(cliente: TestClient, cambios: dict):
    proyecto = crear_proyecto(cliente)
    actividad = crear_actividad(cliente, proyecto["id"])

    respuesta = cliente.put(f"/actividades/{actividad['id']}", json=datos_actividad(**cambios))

    assert respuesta.status_code == 422


def test_eliminar_actividad_devuelve_204_y_desaparece_de_la_lista(cliente: TestClient):
    proyecto = crear_proyecto(cliente)
    actividad = crear_actividad(cliente, proyecto["id"], nombre="A borrar")
    crear_actividad(cliente, proyecto["id"], nombre="Se queda")

    respuesta = cliente.delete(f"/actividades/{actividad['id']}")

    assert respuesta.status_code == 204
    restantes = cliente.get(f"/proyectos/{proyecto['id']}/actividades").json()
    assert [item["nombre"] for item in restantes] == ["Se queda"]


def test_eliminar_actividad_inexistente_devuelve_404(cliente: TestClient):
    respuesta = cliente.delete(f"/actividades/{ACTIVIDAD_INEXISTENTE}")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": MENSAJE_ACTIVIDAD_INEXISTENTE}
