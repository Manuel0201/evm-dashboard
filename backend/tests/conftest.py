"""Preparación compartida de las pruebas: una base PostgreSQL de pruebas, limpia en cada prueba."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.base_de_datos import obtener_url_base_de_datos

NOMBRE_BASE_DE_PRUEBAS = "evm_db_test"
SCRIPT_INICIALIZACION = Path(__file__).resolve().parents[2] / "database" / "init.sql"


@pytest.fixture(scope="session")
def motor_pruebas() -> Iterator[Engine]:
    url = make_url(obtener_url_base_de_datos()).set(database=NOMBRE_BASE_DE_PRUEBAS)
    motor = create_engine(url)
    yield motor
    motor.dispose()


@pytest.fixture
def preparar_tablas(motor_pruebas: Engine) -> None:
    """Borra las tablas y las crea de nuevo con el script real de inicialización."""
    with motor_pruebas.begin() as conexion:
        conexion.execute(text("DROP TABLE IF EXISTS actividades, proyectos"))
        conexion.exec_driver_sql(SCRIPT_INICIALIZACION.read_text(encoding="utf-8"))


@pytest.fixture
def sesion(motor_pruebas: Engine, preparar_tablas: None) -> Iterator[Session]:
    with Session(motor_pruebas) as sesion_de_prueba:
        yield sesion_de_prueba
