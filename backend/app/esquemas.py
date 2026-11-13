"""Esquemas del API: la forma de lo que entra (validado) y de lo que sale en el JSON."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer, StringConstraints

from app.calculos.tipos import InterpretacionCosto, InterpretacionCronograma
from app.constantes import (
    DECIMALES,
    DIGITOS_DINERO,
    DIGITOS_PORCENTAJE,
    LONGITUD_NOMBRE,
    MONTO_MINIMO,
    PORCENTAJE_MAXIMO,
    PORCENTAJE_MINIMO,
)

Nombre = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=LONGITUD_NOMBRE)
]
Porcentaje = Annotated[
    Decimal,
    Field(
        ge=PORCENTAJE_MINIMO,
        le=PORCENTAJE_MAXIMO,
        max_digits=DIGITOS_PORCENTAJE,
        decimal_places=DECIMALES,
        description="Porcentaje de 0 a 100",
    ),
]
Dinero = Annotated[
    Decimal,
    Field(ge=MONTO_MINIMO, max_digits=DIGITOS_DINERO, decimal_places=DECIMALES),
]
NumeroEnJson = Annotated[Decimal, PlainSerializer(float, return_type=float, when_used="json")]


class ProyectoEntrada(BaseModel):
    nombre: Nombre = Field(description="Nombre del proyecto", examples=["Migración de facturación"])


class ProyectoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str


class ActividadEntrada(BaseModel):
    nombre: Nombre = Field(description="Nombre de la actividad", examples=["Desarrollar el bot"])
    presupuesto_total: Dinero = Field(description="BAC: presupuesto total planificado")
    porcentaje_planificado: Porcentaje = Field(
        description="Avance planificado a la fecha de corte (0 a 100)"
    )
    porcentaje_real: Porcentaje = Field(description="Avance real completado (0 a 100)")
    costo_real: Dinero = Field(description="AC: costo real incurrido hasta la fecha")


class IndicadoresSalida(BaseModel):
    """Indicadores EVM. Un valor null significa que no se puede calcular (división por cero)."""

    model_config = ConfigDict(from_attributes=True)

    valor_planificado: NumeroEnJson = Field(description="PV = % planificado x BAC")
    valor_ganado: NumeroEnJson = Field(description="EV = % completado x BAC")
    variacion_costo: NumeroEnJson = Field(description="CV = EV - AC")
    variacion_cronograma: NumeroEnJson = Field(description="SV = EV - PV")
    cpi: NumeroEnJson | None = Field(description="CPI = EV / AC")
    spi: NumeroEnJson | None = Field(description="SPI = EV / PV")
    eac: NumeroEnJson | None = Field(description="EAC = BAC / CPI")
    vac: NumeroEnJson | None = Field(description="VAC = BAC - EAC")
    interpretacion_costo: InterpretacionCosto
    interpretacion_cronograma: InterpretacionCronograma


class ActividadSalida(BaseModel):
    id: int
    proyecto_id: int
    nombre: str
    presupuesto_total: NumeroEnJson
    porcentaje_planificado: NumeroEnJson
    porcentaje_real: NumeroEnJson
    costo_real: NumeroEnJson
    indicadores: IndicadoresSalida


class ErrorSalida(BaseModel):
    detail: str = Field(examples=["Proyecto 7 no existe"])
