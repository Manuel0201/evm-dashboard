"""Pruebas de integración del endpoint de indicadores consolidados del proyecto."""

from fastapi.testclient import TestClient

from tests.ayudas import CLAVES_INDICADORES, crear_actividad, crear_proyecto

PROYECTO_INEXISTENTE = 999999


def test_indicadores_consolidan_sumando_montos_y_recalculando_indices(cliente: TestClient):
    proyecto = crear_proyecto(cliente)
    crear_actividad(cliente, proyecto["id"], nombre="A")
    crear_actividad(
        cliente,
        proyecto["id"],
        nombre="B",
        presupuesto_total=3000,
        porcentaje_planificado=50,
        porcentaje_real=60,
        costo_real=1500,
    )

    respuesta = cliente.get(f"/proyectos/{proyecto['id']}/indicadores")

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert set(cuerpo) == CLAVES_INDICADORES
    assert cuerpo == {
        "valor_planificado": 2000,
        "valor_ganado": 2200,
        "variacion_costo": 100,
        "variacion_cronograma": 200,
        "cpi": 1.0476,
        "spi": 1.1,
        "eac": 3818.18,
        "vac": 181.82,
        "interpretacion_costo": "Bajo presupuesto",
        "interpretacion_cronograma": "Adelantado",
    }


def test_indicadores_de_proyecto_sin_actividades_no_son_calculables(cliente: TestClient):
    proyecto = crear_proyecto(cliente)

    respuesta = cliente.get(f"/proyectos/{proyecto['id']}/indicadores")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "valor_planificado": 0,
        "valor_ganado": 0,
        "variacion_costo": 0,
        "variacion_cronograma": 0,
        "cpi": None,
        "spi": None,
        "eac": None,
        "vac": None,
        "interpretacion_costo": "No calculable",
        "interpretacion_cronograma": "No calculable",
    }


def test_indicadores_se_actualizan_al_editar_una_actividad(cliente: TestClient):
    proyecto = crear_proyecto(cliente)
    actividad = crear_actividad(cliente, proyecto["id"])
    cambios = {
        "nombre": actividad["nombre"],
        "presupuesto_total": 1000,
        "porcentaje_planificado": 50,
        "porcentaje_real": 50,
        "costo_real": 500,
    }

    cliente.put(f"/actividades/{actividad['id']}", json=cambios)
    cuerpo = cliente.get(f"/proyectos/{proyecto['id']}/indicadores").json()

    assert cuerpo["cpi"] == 1
    assert cuerpo["spi"] == 1
    assert cuerpo["interpretacion_costo"] == "En presupuesto"
    assert cuerpo["interpretacion_cronograma"] == "En tiempo"


def test_indicadores_ignoran_las_actividades_de_otros_proyectos(cliente: TestClient):
    proyecto_uno = crear_proyecto(cliente, "Uno")
    proyecto_dos = crear_proyecto(cliente, "Dos")
    crear_actividad(cliente, proyecto_uno["id"])
    crear_actividad(cliente, proyecto_dos["id"], presupuesto_total=5000)

    cuerpo = cliente.get(f"/proyectos/{proyecto_uno['id']}/indicadores").json()

    assert cuerpo["valor_planificado"] == 500


def test_indicadores_de_proyecto_inexistente_devuelven_404(cliente: TestClient):
    respuesta = cliente.get(f"/proyectos/{PROYECTO_INEXISTENTE}/indicadores")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Proyecto 999999 no existe"}
