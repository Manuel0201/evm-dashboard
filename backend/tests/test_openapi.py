"""Pruebas de la documentación OpenAPI: ruta, descripciones, esquemas y códigos de error."""

import pytest
from fastapi.testclient import TestClient

from app.main import RUTA_DOCUMENTACION, crear_aplicacion

RUTA_ESPECIFICACION = "/openapi.json"
METODOS_HTTP = {"get", "post", "put", "delete"}
CODIGOS_DE_ERROR_POR_ENDPOINT = {
    ("post", "/proyectos"): {"201", "422"},
    ("get", "/proyectos"): {"200"},
    ("get", "/proyectos/{proyecto_id}"): {"200", "404", "422"},
    ("put", "/proyectos/{proyecto_id}"): {"200", "404", "422"},
    ("delete", "/proyectos/{proyecto_id}"): {"204", "404", "422"},
    ("get", "/proyectos/{proyecto_id}/indicadores"): {"200", "404", "422"},
    ("post", "/proyectos/{proyecto_id}/actividades"): {"201", "404", "422"},
    ("get", "/proyectos/{proyecto_id}/actividades"): {"200", "404", "422"},
    ("put", "/actividades/{actividad_id}"): {"200", "404", "422"},
    ("delete", "/actividades/{actividad_id}"): {"204", "404", "422"},
}


@pytest.fixture(scope="module")
def cliente_sin_base_de_datos() -> TestClient:
    return TestClient(crear_aplicacion())


@pytest.fixture(scope="module")
def especificacion(cliente_sin_base_de_datos: TestClient) -> dict:
    return cliente_sin_base_de_datos.get(RUTA_ESPECIFICACION).json()


def listar_operaciones(especificacion: dict) -> list[tuple[str, str, dict]]:
    return [
        (metodo, ruta, operacion)
        for ruta, metodos in especificacion["paths"].items()
        for metodo, operacion in metodos.items()
        if metodo in METODOS_HTTP
    ]


def test_la_documentacion_esta_en_api_docs(cliente_sin_base_de_datos: TestClient):
    respuesta = cliente_sin_base_de_datos.get(RUTA_DOCUMENTACION)

    assert RUTA_DOCUMENTACION == "/api-docs"
    assert respuesta.status_code == 200
    assert "swagger" in respuesta.text.lower()


def test_la_ruta_docs_por_defecto_ya_no_existe(cliente_sin_base_de_datos: TestClient):
    assert cliente_sin_base_de_datos.get("/docs").status_code == 404


def test_la_especificacion_describe_la_api(especificacion: dict):
    assert especificacion["info"]["title"] == "EVM Dashboard API"
    assert "Valor Ganado" in especificacion["info"]["description"]


def test_documenta_exactamente_los_diez_endpoints_esperados(especificacion: dict):
    documentados = {(metodo, ruta) for metodo, ruta, _ in listar_operaciones(especificacion)}

    assert documentados == set(CODIGOS_DE_ERROR_POR_ENDPOINT)


def test_cada_endpoint_tiene_resumen_y_descripcion(especificacion: dict):
    for metodo, ruta, operacion in listar_operaciones(especificacion):
        assert operacion.get("summary"), f"{metodo} {ruta} sin resumen"
        assert operacion.get("description"), f"{metodo} {ruta} sin descripción"


def test_cada_endpoint_documenta_sus_codigos_de_respuesta_y_error(especificacion: dict):
    for metodo, ruta, operacion in listar_operaciones(especificacion):
        esperados = CODIGOS_DE_ERROR_POR_ENDPOINT[(metodo, ruta)]
        assert set(operacion["responses"]) == esperados, f"{metodo} {ruta}"


def test_los_errores_404_tienen_esquema_con_detalle(especificacion: dict):
    esquema = especificacion["components"]["schemas"]["ErrorSalida"]

    assert "detail" in esquema["properties"]


def test_los_endpoints_que_reciben_datos_documentan_el_esquema_de_la_peticion(
    especificacion: dict,
):
    for metodo, ruta, operacion in listar_operaciones(especificacion):
        if metodo in {"post", "put"}:
            esquema = operacion["requestBody"]["content"]["application/json"]["schema"]
            assert "$ref" in esquema, f"{metodo} {ruta} sin esquema de petición"


def test_los_endpoints_que_devuelven_datos_documentan_el_esquema_de_la_respuesta(
    especificacion: dict,
):
    for metodo, ruta, operacion in listar_operaciones(especificacion):
        codigo_exitoso = next(codigo for codigo in operacion["responses"] if codigo.startswith("2"))
        if codigo_exitoso != "204":
            contenido = operacion["responses"][codigo_exitoso]["content"]["application/json"]
            assert "$ref" in contenido["schema"] or "items" in contenido["schema"], (
                f"{metodo} {ruta} sin esquema de respuesta"
            )


def test_los_indicadores_documentan_los_valores_posibles_de_la_interpretacion(
    especificacion: dict,
):
    esquemas = especificacion["components"]["schemas"]

    assert set(esquemas["InterpretacionCosto"]["enum"]) == {
        "Bajo presupuesto",
        "En presupuesto",
        "Sobre presupuesto",
        "No calculable",
    }
    assert set(esquemas["InterpretacionCronograma"]["enum"]) == {
        "Adelantado",
        "En tiempo",
        "Atrasado",
        "No calculable",
    }
