"""Conexión a PostgreSQL. La dirección (con la contraseña) se lee del archivo .env."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
VARIABLE_URL_BASE_DE_DATOS = "DATABASE_URL"
PREFIJO_URL_POSTGRES = "postgresql://"
PREFIJO_URL_PSYCOPG = "postgresql+psycopg://"


class Base(DeclarativeBase):
    """Clase de la que heredan todos los modelos (tablas)."""


def obtener_url_base_de_datos() -> str:
    """Lee DATABASE_URL del .env y la adapta al conector psycopg."""
    load_dotenv(RAIZ_PROYECTO / ".env")
    url = os.environ.get(VARIABLE_URL_BASE_DE_DATOS)
    if url is None:
        raise RuntimeError(f"Falta {VARIABLE_URL_BASE_DE_DATOS}: copia .env.example a .env")
    return url.replace(PREFIJO_URL_POSTGRES, PREFIJO_URL_PSYCOPG, 1)


def crear_motor(url: str) -> Engine:
    """Crea la conexión (motor) hacia la base de datos."""
    return create_engine(url)


def crear_fabrica_sesiones(motor: Engine) -> sessionmaker[Session]:
    """Crea la fábrica de sesiones: cada sesión es una 'conversación' con la base."""
    return sessionmaker(bind=motor)
